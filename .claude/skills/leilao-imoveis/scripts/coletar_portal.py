#!/usr/bin/env python3
"""Coleta lotes da Caixa por cidade usando os endpoints internos do portal.

    python3 coletar_portal.py SC 8761:PALHOCA lista.csv
    python3 coletar_portal.py SC 8873:SAO_JOSE 8621:FLORIANOPOLIS anel2.csv

O codigo da cidade sai de carregaListaCidades.asp (POST cmb_estado=UF).

O download estatico (/listaweb/Lista_imoveis_UF.csv) e barrado pelo bot manager
do portal neste ambiente; os endpoints POST que o proprio formulario usa passam.
Gera CSV no formato que scripts/triagem.py consome.
"""
import csv, html, os, re, subprocess, sys, tempfile, time

BASE = "https://venda-imoveis.caixa.gov.br/sistema"
RAIZ = "https://venda-imoveis.caixa.gov.br"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
# O portal exige cookie de sessao: sem ele os endpoints devolvem 302 para o
# validador antirrobo. Um arquivo por execucao basta.
CJ = os.path.join(tempfile.gettempdir(), "caixa-cookies-%d.txt" % os.getpid())


def curl(url, data=None, tentativas=4):
    for n in range(tentativas):
        cmd = ["curl", "-sS", "--max-time", "60", "-b", CJ, "-c", CJ,
               "-H", "User-Agent: " + UA,
               "-H", "Referer: %s/busca-imovel.asp" % BASE]
        if data is not None:
            cmd += ["-X", "POST", "--data", data,
                    "-H", "Content-Type: application/x-www-form-urlencoded; charset=UTF-8",
                    "-H", "X-Requested-With: XMLHttpRequest"]
        cmd.append(url)
        r = subprocess.run(cmd, capture_output=True)
        try:
            txt = r.stdout.decode("utf-8")
        except UnicodeDecodeError:
            txt = r.stdout.decode("latin-1", "replace")
        if "302 Found" not in txt and len(txt) > 50:
            return txt
        time.sleep(2 * (n + 1))          # bot manager: recua e tenta de novo
    return ""


def limpar(t):
    t = re.sub(r"<[^>]+>", " ", t or "")
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def campo(src, rotulo):
    m = re.search(rotulo + r"\s*:?\s*=?\s*<strong>(.*?)</strong>", src, re.S | re.I)
    return limpar(m.group(1)) if m else ""


def num(t):
    try:
        return float(str(t).replace(".", "").replace(",", "."))
    except ValueError:
        return 0.0


def modalidade(d, rx):
    """Le a modalidade do lote.

    Leilao SFI e Licitacao Aberta trazem um bloco de titulo com o nome do
    certame. Venda Online e Venda Direta nao trazem bloco nenhum -- a pagina
    so se distingue pelos endpoints que usa. Sem isto a modalidade sai vazia
    e o triagem.py pontua o lote com a nota neutra, justamente nas duas
    modalidades que o mandato prefere.
    """
    titulo = rx(r"font-size: 14pt;'><b>(.*?)</b>")
    if titulo:
        return titulo
    if "/venda-online/" in d or "Fazer uma proposta" in d:
        return "Venda Online"
    if "venda-direta" in d or "Compra Direta" in d:
        return "Venda Direta"
    return ""


def extrai(d, cod, uf, nome_cidade):
    def rx(p, g=1):
        m = re.search(p, d, re.S)
        return limpar(m.group(g)) if m else ""

    aval = rx(r"Valor de avalia\w+o:\s*R\$\s*([\d.,]+)")
    p_unico = rx(r"Valor m\w+nimo de venda:\s*(?:</?b>\s*)?R\$\s*([\d.,]+)")
    p1 = rx(r"Valor m\w+nimo de venda 1\w+ Leil\w+o:\s*R\$\s*([\d.,]+)")
    p2 = rx(r"Valor m\w+nimo de venda 2\w+ Leil\w+o:\s*R\$\s*([\d.,]+)")
    preco = p_unico or p2 or p1                  # piso efetivo de entrada
    desc = rx(r"desconto de ([\d.,]+)%")
    if not desc and num(aval) and num(preco):
        desc = ("%.2f" % ((1 - num(preco) / num(aval)) * 100)).replace(".", ",")

    end = rx(r"<strong>Endere\w+o:</strong><br>(.*?)</p>")
    mb = re.search(r",\s*([^,]+?)\s*-\s*CEP:", end)
    bairro = mb.group(1).strip() if mb else ""
    mpdf = re.search(r"ExibeDoc\('([^']*matricula[^']*)'\)", d)
    medt = re.search(r"ExibeDoc\('(/editais/(?!matricula)[^']*?\.PDF)'\)", d, re.I)
    mplat = re.search(r'SiteLeiloeiro\("([^"]+)"\)', d)
    datas = re.findall(r"Data d[aoe][^<]*?-\s*(\d{2}/\d{2}/\d{4})[^<]*", d)
    # O portal traz a situacao de ocupacao dentro de um comentario HTML: nao
    # aparece na tela, mas esta na fonte e e' informacao declarada pela Caixa.
    situacao = rx(r"Situa\w+o:\s*<strong>(.*?)</strong>")

    return {
        "Numero do imovel": campo(d, r"N\w+mero do im\w+vel") or cod,
        "UF": uf, "Cidade": nome_cidade, "Bairro": bairro, "Endereco": end,
        "Preco": preco, "Valor de avaliacao": aval, "Desconto": desc,
        "Preco 1o leilao": p1, "Preco 2o leilao": p2,
        "Tipo": campo(d, r"Tipo de im\w+vel"),
        "Quartos": campo(d, r"Quartos"),
        "Garagem": campo(d, r"Garagem"),
        "Area total": campo(d, r"\w+rea total"),
        "Area privativa": campo(d, r"\w+rea privativa"),
        "Matricula": campo(d, r"Matr\w+cula\(s\)"),
        "Comarca": campo(d, r"Comarca"),
        "Oficio": campo(d, r"Of\w+cio"),
        "Situacao": situacao,
        # A situacao entra tambem na descricao porque e' dali que o triagem.py
        # le a ocupacao. Sem isso todo lote sai como DESCONHECIDO.
        "Descricao": (rx(r"<strong>Descri\w+o:</strong><br>(.*?)</p>")
                      + " " + situacao).strip(),
        "Modalidade": modalidade(d, rx),
        "Edital": rx(r"Edital:&nbsp;([^<]+)"),
        "Leiloeiro": rx(r"Leiloeiro\(a\):\s*([^<]+)"),
        "Plataforma": mplat.group(1) if mplat else "",
        "Data certame": " / ".join(datas),
        "Condominio (regra)": rx(r"Condom\w+nio:\s*([^<]+)"),
        "Tributos (regra)": rx(r"Tributos:\s*([^<]+)"),
        "Formas de pagamento": rx(r"FORMAS DE PAGAMENTO ACEITAS:(.*?)REGRAS PARA"),
        "Aceita FGTS": "SIM" if re.search(r"utiliza\w+o de FGTS", d) else "NAO",
        "Aceita financiamento": "SIM" if re.search(
            r"[Ff]inanciamento habitacional|Permite financiamento|parcelad", d) else "NAO",
        "Matricula PDF": (RAIZ + mpdf.group(1)) if mpdf else "",
        "Edital PDF": (RAIZ + medt.group(1)) if medt else "",
        "Link": "%s/detalhe-imovel.asp?hdnimovel=%s" % (BASE, cod),
    }


class ColetaIncompleta(RuntimeError):
    """O portal listou o lote e nao entregou o detalhe. Nunca confundir com
    lote que saiu da lista."""


ESSENCIAIS = ("Bairro", "Preco", "Valor de avaliacao", "Area privativa")


def completa(linha):
    """A pagina de detalhe as vezes responde 200 com o corpo vazio. O curl()
    aceita (nao e' 302 e tem corpo), o extrai() devolve a linha toda em branco
    e o lote entra na planilha sem bairro e sem preco -- que a triagem descarta
    como fora_do_bairro e o diff le como alteracao. Linha incompleta nao e'
    dado: ou se recoleta, ou a rodada falha em voz alta."""
    return all(linha.get(c) for c in ESSENCIAIS)


def coletar_detalhe(cod, uf, nome_cidade, tentativas=4):
    for n in range(tentativas):
        d = curl(BASE + "/detalhe-imovel.asp", "hdnImovel=%s&hdnOrigem=index" % cod)
        if d:
            linha = extrai(d, cod, uf, nome_cidade)
            if completa(linha):
                return linha
        time.sleep(1.5 * (n + 1))
    return None


def buscar_ids(uf, cod_cidade, tentativas=4):
    """Devolve os codigos dos lotes que a busca lista para a cidade.

    A busca responde 200 com zero lotes de forma intermitente: em 04/10/2026
    Florianopolis veio vazia tres vezes e completa na quarta, com dois lotes
    inalterados. Zero lote e' praca vazia ou antirrobo, e daqui as duas se
    parecem -- por isso se repete a consulta antes de concluir que esta vazia,
    com a sessao reaquecida a cada volta."""
    for n in range(tentativas):
        curl(BASE + "/busca-imovel.asp")                   # aquece a sessao
        pesq = curl(BASE + "/carregaPesquisaImoveis.asp",
                    "hdn_estado=%s&hdn_cidade=%s&hdn_bairro=&hdn_tp_imovel=Selecione"
                    "&hdn_area_util=&hdn_faixa_vlr=&hdn_quartos=&hdn_vg_garagem="
                    "&hdn_modalidade=&strValorSimulador=&strAceitaFGTS="
                    "&strAceitaFinanciamento=" % (uf, cod_cidade))
        ids = []
        for v in re.findall(r"hdnImov\d+'\s+value=([\d_]+)", pesq):
            ids += [x for x in v.split("_") if x.strip()]
        if ids:
            return sorted(set(ids)), n + 1
        time.sleep(2.0 * (n + 1))
    return [], tentativas


def coletar(uf, cod_cidade, nome_cidade):
    ids, voltas = buscar_ids(uf, cod_cidade)
    if not ids:
        raise ColetaIncompleta(
            "%s/%s: a busca nao devolveu lote nenhum em %d tentativas. Pode ser "
            "praca vazia, pode ser o antirrobo barrando a consulta -- e daqui as "
            "duas se parecem. Nada foi gravado." % (nome_cidade, uf, voltas))
    print("%s/%s: %d lotes no portal%s" % (
        nome_cidade, uf, len(ids),
        "" if voltas == 1 else " (busca vazia em %d tentativa(s) antes)" % (voltas - 1)),
        file=sys.stderr)

    linhas, falhos = [], []
    for i, cod in enumerate(ids, 1):
        linha = coletar_detalhe(cod, uf, nome_cidade)
        if linha is None:
            falhos.append(cod)
            print("  [%d/%d] %s FALHOU - detalhe incompleto em 4 tentativas"
                  % (i, len(ids), cod), file=sys.stderr)
            continue
        linhas.append(linha)
        print("  [%d/%d] %-14s %-22s %-12s %s" % (
            i, len(ids), cod, linha["Bairro"][:22], linha["Preco"],
            linha["Modalidade"][:20]), file=sys.stderr)
        time.sleep(0.4)

    if falhos:
        raise ColetaIncompleta(
            "%s/%s: %d de %d lotes sem detalhe (%s). O portal listou o lote e "
            "nao entregou a pagina. Nada foi gravado: lista parcial faria o "
            "diff acusar saida que nao houve."
            % (nome_cidade, uf, len(falhos), len(ids), ", ".join(falhos)))
    return linhas


if __name__ == "__main__":
    uf, saida = sys.argv[1], sys.argv[-1]
    todas = []
    try:
        for par in sys.argv[2:-1]:
            cod, nome = par.split(":", 1)
            todas += coletar(uf, cod, nome)
    except ColetaIncompleta as e:
        print("FALHA NA COLETA DO PORTAL: %s" % e, file=sys.stderr)
        sys.exit(2)
    if todas:
        with open(saida, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(todas[0].keys()), delimiter=";")
            w.writeheader(); w.writerows(todas)
        print("gravado %s (%d lotes)" % (saida, len(todas)), file=sys.stderr)
