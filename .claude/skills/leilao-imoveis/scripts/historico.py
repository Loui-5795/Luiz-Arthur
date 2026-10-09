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

    # Quem estava em quarentena e voltou a aparecer nunca saiu. Limpa sem registrar.
    voltaram = [i for i in quarentena if i in agora]
    for i in voltaram:
        del quarentena[i]

    # Ausente = estava na coleta anterior ou na quarentena, e nao esta na atual.
    # O criterio e' a ausencia na coleta ATUAL -- nunca a diferenca entre duas
    # coletas, que deixava o lote preso na quarentena para sempre.
    ausentes = {k: v for k, v in antes.items() if k not in agora}

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
    ja_ids = {r[1] for r in ja}
    novas = [r for r in confirmadas if r["id"] not in ja_ids]

    existe = os.path.exists(a.historico)
    with open(a.historico, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS, delimiter=";")
        if not existe:
            w.writeheader()
        w.writerows(novas)
    gravar_quarentena(a.quarentena, quarentena)

    print("%d ausente(s) nesta rodada | %d saida(s) confirmada(s) | %d em quarentena"
          % (len(ausentes), len(novas), len(quarentena)))
    for r in novas:
        print("  SAIU       %s  %-16s %-18s %-13s R$ %s" % (
            r["data_saida"], r["id"], r["bairro"][:18], r["cidade"], r["ultimo_preco"]))
    for r in novas_em_quarentena:
        print("  1a falta   %s  %-16s %-18s %-13s R$ %s  (aguarda 2a rodada)" % (
            r["primeira_ausencia"], r["id"], r["bairro"][:18], r["cidade"],
            r["ultimo_preco"]))
    for i in voltaram:
        print("  REAPARECEU %-16s  nunca saiu; retirado da quarentena" % i)


if __name__ == "__main__":
    main()
