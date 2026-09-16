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
        "Situacao": rx(r"Situa\w+o:\s*<strong>(.*?)</strong>"),
        "Descricao": rx(r"<strong>Descri\w+o:</strong><br>(.*?)</p>"),
        "Modalidade": rx(r"font-size: 14pt;'><b>(.*?)</b>"),
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


def coletar(uf, cod_cidade, nome_cidade):
    curl(BASE + "/busca-imovel.asp")                       # aquece a sessao
    pesq = curl(BASE + "/carregaPesquisaImoveis.asp",
                "hdn_estado=%s&hdn_cidade=%s&hdn_bairro=&hdn_tp_imovel=Selecione"
                "&hdn_area_util=&hdn_faixa_vlr=&hdn_quartos=&hdn_vg_garagem="
                "&hdn_modalidade=&strValorSimulador=&strAceitaFGTS="
                "&strAceitaFinanciamento=" % (uf, cod_cidade))
    ids = []
    for v in re.findall(r"hdnImov\d+'\s+value=([\d_]+)", pesq):
        ids += [x for x in v.split("_") if x.strip()]
    ids = sorted(set(ids))
    print("%s/%s: %d lotes no portal" % (nome_cidade, uf, len(ids)), file=sys.stderr)

    linhas = []
    for i, cod in enumerate(ids, 1):
        d = curl(BASE + "/detalhe-imovel.asp", "hdnImovel=%s&hdnOrigem=index" % cod)
        if not d:
            print("  [%d/%d] %s FALHOU" % (i, len(ids), cod), file=sys.stderr)
            continue
        linha = extrai(d, cod, uf, nome_cidade)
        linhas.append(linha)
        print("  [%d/%d] %-14s %-22s %-12s %s" % (
            i, len(ids), cod, linha["Bairro"][:22], linha["Preco"],
            linha["Modalidade"][:20]), file=sys.stderr)
        time.sleep(0.4)
    return linhas


if __name__ == "__main__":
    uf, saida = sys.argv[1], sys.argv[-1]
    todas = []
    for par in sys.argv[2:-1]:
        cod, nome = par.split(":", 1)
        todas += coletar(uf, cod, nome)
    if todas:
        with open(saida, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(todas[0].keys()), delimiter=";")
            w.writeheader(); w.writerows(todas)
        print("gravado %s (%d lotes)" % (saida, len(todas)), file=sys.stderr)
