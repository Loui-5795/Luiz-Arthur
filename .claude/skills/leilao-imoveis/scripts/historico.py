#!/usr/bin/env python3
"""Registra os lotes que sairam da lista do portal entre duas coletas.

    python3 historico.py --anterior dados/lotes-A.csv --atual dados/lotes-B.csv \
                         --historico dados/historico-saidas.csv \
                         --quarentena dados/ausencias-pendentes.csv \
                         --data 19/09/2026

O triagem.py reescreve o pipeline.csv a cada rodada a partir da lista corrente,
entao lote que sai do portal desaparece do historico. E justamente esse o dado
que calibra lance futuro: quantos lotes da praca sumiram, de que faixa de preco
e depois de qual data de certame. Este script preserva isso, sem apagar nada.

O portal nao diz se o lote saiu por arremate, suspensao ou retirada. O registro
guarda o fato observado -- saiu da lista -- e nunca supoe a causa.

LOTE QUE VOLTA. Sair da lista nao e' estado permanente: um lote pode ser
reofertado semanas depois, em edital novo e as vezes em OUTRA modalidade. Em
13/11/2026 anunciei como "lote novo" o 855551517677-2, do Rocado, que de fato
era um retorno -- havia saido em 19/09, como Leilao SFI, e voltou como
Licitacao Aberta. A conferencia existia (o historico) e eu nao a fiz. Agora o
script a faz: todo lote que aparece e' cruzado com o historico de saidas, e o
retorno e' anunciado como retorno, com a comparacao de preco e modalidade.

REGRA DAS DUAS RODADAS. Em 02/10/2026 um lote de Venda Online foi registrado
como saida e reapareceu intacto na rodada seguinte: a ausencia era
indisponibilidade da fonte, nao saida. Uma retratacao depois, a regra passou a
ser esta: a primeira ausencia nao vale saida, vai para a quarentena. Confirma-se
a saida quando o lote falta em duas rodadas consecutivas. Reaparecendo, sai da
quarentena sem nunca ter sujado o historico.
"""
import argparse, csv, os, re

CAMPOS = ["data_saida", "id", "cidade", "bairro", "endereco", "tipo",
          "area_privativa", "valor_avaliacao", "ultimo_preco", "modalidade",
          "situacao", "datas_certame", "edital", "observacao"]

CAMPOS_Q = ["primeira_rodada", "primeira_ausencia", "id", "cidade", "bairro",
            "endereco", "tipo",
            "area_privativa", "valor_avaliacao", "ultimo_preco", "modalidade",
            "situacao", "datas_certame", "edital"]


def rodada_de(caminho):
    """Identifica a rodada pelo nome do arquivo de coleta, nao pela data.

    A data NAO identifica uma rodada: ha duas por dia, as 07h e as 19h, e em
    09/10/2026 foi exatamente isso que quebrou a regra das duas rodadas. Um
    lote ausente pela primeira vez as 19h foi confirmado como saida na mesma
    rodada, porque a quarentena so' guardava "09/10/2026" e a comparacao com a
    data corrente nao distinguia manha de noite. O nome do arquivo distingue."""
    m = re.search(r"(\d{4}-\d{2}-\d{2}(?:-\d{2}h)?)", os.path.basename(caminho))
    return m.group(1) if m else os.path.basename(caminho)


def valor(t):
    try:
        return float(str(t).replace(".", "").replace(",", "."))
    except (ValueError, AttributeError):
        return 0.0


def ler(caminho):
    with open(caminho, encoding="utf-8-sig") as f:
        return {r["Numero do imovel"]: r for r in csv.DictReader(f, delimiter=";")}


def ler_quarentena(caminho):
    if not caminho or not os.path.exists(caminho):
        return {}
    with open(caminho, encoding="utf-8-sig") as f:
        return {r["id"]: r for r in csv.DictReader(f, delimiter=";")}


def gravar_quarentena(caminho, registros):
    if not caminho:
        return
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS_Q, delimiter=";")
        w.writeheader()
        w.writerows(registros.values())


def sem_certame(r):
    """Lote sem data de certame -- Venda Online, oferta continua por proposta.

    Em 16/10/2026 ficou demonstrado que, para esses lotes, **ausencia da lista
    nao e' prova de saida**. O lote 144440299841-6, apartamento no Centro de
    Florianopolis, ficou ausente por TREZE rodadas consecutivas, teve a saida
    confirmada pela regra das duas rodadas, e reapareceu intacto na decima
    quarta. Nenhuma janela finita de confirmacao o teria poupado.

    O placar e' inequivoco: dos dois registros de Venda Online que chegaram ao
    historico, **os dois eram falsos**. Dos quatorze de Leilao SFI, nenhum.
    A explicacao e' estrutural: o lote com certame sai da lista por um evento
    datado, e o de oferta continua some e volta ao sabor do processamento de
    propostas.

    Dai a regra: lote sem data de certame nao entra no historico de saidas.
    Vai para um registro proprio de ausencias, que descreve o que se observou
    -- ausente -- e nao afirma o que nao se sabe."""
    return not (r.get("Data certame") or "").strip()


def do_portal(r, data):
    """Extrai de um registro do portal os campos do historico."""
    return {
        "data_saida": data, "id": r["Numero do imovel"],
        "cidade": r.get("Cidade", ""), "bairro": r.get("Bairro", ""),
        "endereco": r.get("Endereco", ""), "tipo": r.get("Tipo", ""),
        "area_privativa": r.get("Area privativa", ""),
        "valor_avaliacao": r.get("Valor de avaliacao", ""),
        "ultimo_preco": r.get("Preco", ""), "modalidade": r.get("Modalidade", ""),
        "situacao": r.get("Situacao", ""), "datas_certame": r.get("Data certame", ""),
        "edital": r.get("Edital", ""),
    }


def dias_do_certame(registro, data_saida):
    """Dias entre o 1o certame do lote e a sua ausencia.

    Medido em 24/11/2026 sobre as vinte e uma saidas confirmadas: dezenove
    ocorreram DEPOIS do certame, e o intervalo se agrupa por modalidade --
    Leilao SFI sai de +5 a +7 dias do 1o leilao (isto e', depois do 2o);
    Licitacao Aberta sai em +1 dia, em cinco casos de cinco.

    Serve de alarme nos dois sentidos: ausencia muito antes do certame pede
    conferencia na fonte, e lote de Licitacao Aberta que PERMANECE dois dias
    apos o certame tambem e' anomalia. Por isso a relacao se imprime no
    momento do evento, e nao apenas no relatorio de depois.
    """
    import datetime, re
    def ds(t):
        return sorted(datetime.date(int(y), int(m), int(d)) for d, m, y in
                      (x.groups() for x in re.finditer(r"(\d{2})/(\d{2})/(\d{4})", t or "")))
    certames = ds(registro.get("datas_certame", ""))
    saida = ds(data_saida)
    if not certames or not saida:
        return None
    return (saida[0] - certames[0]).days


def relacao_certame(registro, data_saida):
    d = dias_do_certame(registro, data_saida)
    if d is None:
        return "sem data de certame registrada"
    if d > 0:
        return "%+d dia(s) do 1o certame (%s) -- curso esperado" % (
            d, registro.get("datas_certame", "")[:10])
    return "%+d dia(s) do 1o certame (%s) -- ANTES do certame, conferir na fonte" % (
        d, registro.get("datas_certame", "")[:10])


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--anterior", required=True)
    p.add_argument("--atual", required=True)
    p.add_argument("--historico", required=True)
    p.add_argument("--quarentena", help="dados/ausencias-pendentes.csv. Sem este "
                   "argumento a regra das duas rodadas nao se aplica.")
    p.add_argument("--data", required=True)
    a = p.parse_args()

    antes, agora = ler(a.anterior), ler(a.atual)
    rodada = rodada_de(a.atual)
    quarentena = ler_quarentena(a.quarentena)

    # Lote que aparece e ja consta do historico nao e' novo: e' reoferta.
    saiu_antes = {}
    if os.path.exists(a.historico):
        with open(a.historico, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f, delimiter=";"):
                if "RETRATADO" not in r.get("observacao", ""):
                    saiu_antes[r["id"]] = r          # fica a saida mais recente
    retornos = [(i, saiu_antes[i]) for i in agora
                if i not in antes and i in saiu_antes]

    # Quem estava em quarentena e voltou a aparecer nunca saiu. Limpa sem registrar.
    voltaram = [i for i in quarentena if i in agora]
    for i in voltaram:
        del quarentena[i]

    # Ausente = estava na coleta anterior ou na quarentena, e nao esta na atual.
    # O criterio e' a ausencia na coleta ATUAL -- nunca a diferenca entre duas
    # coletas, que deixava o lote preso na quarentena para sempre.
    ausentes = {k: v for k, v in antes.items() if k not in agora}

    # Lote sem certame sai do fluxo de saidas e vai para registro proprio.
    sem_data = {k: v for k, v in ausentes.items() if sem_certame(v)}
    for k in sem_data:
        del ausentes[k]
        quarentena.pop(k, None)

    confirmadas, novas_em_quarentena = [], []

    if not a.quarentena:
        for i, r in ausentes.items():
            reg = do_portal(r, a.data)
            reg["observacao"] = ("saiu da lista do portal; causa nao declarada "
                                 "pela fonte")
            confirmadas.append(reg)
    else:
        for i, r in ausentes.items():
            if i not in quarentena:
                q = {c: do_portal(r, a.data).get(c, "") for c in CAMPOS_Q}
                q["primeira_rodada"] = rodada
                q["primeira_ausencia"] = a.data
                quarentena[i] = q
                novas_em_quarentena.append(q)

        # Confirma quem ja faltava numa rodada ANTERIOR a esta e segue ausente.
        for i in [k for k in quarentena if k not in agora]:
            q = quarentena[i]
            if q.get("primeira_rodada", "") == rodada:
                continue            # faltou nesta rodada; aguarda a proxima
            reg = {c: q.get(c, "") for c in CAMPOS}
            reg["data_saida"] = a.data
            reg["id"] = i
            reg["observacao"] = ("saiu da lista do portal; ausente desde %s, "
                                 "confirmado em duas rodadas consecutivas; "
                                 "causa nao declarada pela fonte"
                                 % q["primeira_ausencia"])
            confirmadas.append(reg)
            del quarentena[i]

    ja = set()
    if os.path.exists(a.historico):
        with open(a.historico, encoding="utf-8-sig") as f:
            ja = {(r["data_saida"], r["id"]) for r in csv.DictReader(f, delimiter=";")
                  if "RETRATADO" not in r.get("observacao", "")}
    # Deduplica por (data, lote), nao por lote. Em 11/11/2026 o lote
    # 878771588251-5, de Bela Vista, cuja saida se confirmara em 21/10, voltou
    # a' lista num edital novo, com certames novos. Logo a saida NAO e' estado
    # permanente: o mesmo lote pode sair outra vez, e a chave por lote apagaria
    # silenciosamente a segunda saida -- justamente o dado que mede quantas
    # vezes um lote roda sem ser arrematado.
    novas = [r for r in confirmadas if (r["data_saida"], r["id"]) not in ja]

    existe = os.path.exists(a.historico)
    with open(a.historico, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS, delimiter=";")
        if not existe:
            w.writeheader()
        w.writerows(novas)
    gravar_quarentena(a.quarentena, quarentena)

    if sem_data and a.quarentena:
        reg = os.path.join(os.path.dirname(a.quarentena) or ".",
                           "ausencias-venda-online.csv")
        existe = os.path.exists(reg)
        with open(reg, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["data", "rodada", "id", "cidade",
                                              "bairro", "modalidade", "ultimo_preco",
                                              "observacao"], delimiter=";")
            if not existe:
                w.writeheader()
            for i, r in sem_data.items():
                w.writerow({"data": a.data, "rodada": rodada, "id": i,
                            "cidade": r.get("Cidade", ""), "bairro": r.get("Bairro", ""),
                            "modalidade": r.get("Modalidade", ""),
                            "ultimo_preco": r.get("Preco", ""),
                            "observacao": "ausente da lista; lote sem data de "
                            "certame, cuja ausencia NAO constitui saida"})
        for i, r in sem_data.items():
            print("  SEM CERTAME %-16s %-18s ausente; nao conta como saida"
                  % (i, r.get("Bairro", "")[:18]))

    if retornos:
        reg = os.path.join(os.path.dirname(a.historico) or ".", "retornos.csv")
        existe_r = os.path.exists(reg)
        campos_r = ["data_retorno", "id", "cidade", "bairro", "data_saida_anterior",
                    "modalidade_antes", "modalidade_agora", "preco_antes",
                    "preco_agora", "variacao_pct", "edital_antes", "edital_agora"]
        with open(reg, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=campos_r, delimiter=";")
            if not existe_r:
                w.writeheader()
            for i, ant in retornos:
                at = agora[i]
                pa, pb = valor(ant.get("ultimo_preco")), valor(at.get("Preco"))
                var = ("%.2f" % ((pb / pa - 1) * 100)).replace(".", ",") if pa else ""
                w.writerow({
                    "data_retorno": a.data, "id": i,
                    "cidade": at.get("Cidade", ""), "bairro": at.get("Bairro", ""),
                    "data_saida_anterior": ant.get("data_saida", ""),
                    "modalidade_antes": ant.get("modalidade", ""),
                    "modalidade_agora": at.get("Modalidade", ""),
                    "preco_antes": ant.get("ultimo_preco", ""),
                    "preco_agora": at.get("Preco", ""), "variacao_pct": var,
                    "edital_antes": ant.get("edital", ""),
                    "edital_agora": at.get("Edital", "")})
                print("  RETORNOU   %-16s %-18s saiu em %s como %s a R$ %s; volta "
                      "como %s a R$ %s (%s%%)"
                      % (i, at.get("Bairro", "")[:18], ant.get("data_saida", ""),
                         ant.get("modalidade", ""), ant.get("ultimo_preco", ""),
                         at.get("Modalidade", ""), at.get("Preco", ""), var))

    print("%d ausente(s) nesta rodada | %d saida(s) confirmada(s) | %d em quarentena"
          % (len(ausentes), len(novas), len(quarentena)))
    for r in novas:
        print("  SAIU       %s  %-16s %-18s %-13s R$ %s" % (
            r["data_saida"], r["id"], r["bairro"][:18], r["cidade"], r["ultimo_preco"]))
    for r in novas:
        print("             %s" % relacao_certame(r, r["data_saida"]))
    for r in novas_em_quarentena:
        print("  1a falta   %s  %-16s %-18s %-13s R$ %s  (aguarda 2a rodada)" % (
            r["primeira_ausencia"], r["id"], r["bairro"][:18], r["cidade"],
            r["ultimo_preco"]))
        print("             %s" % relacao_certame(r, r["primeira_ausencia"]))
    for i in voltaram:
        print("  REAPARECEU %-16s  nunca saiu; retirado da quarentena" % i)


if __name__ == "__main__":
    main()
