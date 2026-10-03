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
import argparse, csv, os

CAMPOS = ["data_saida", "id", "cidade", "bairro", "endereco", "tipo",
          "area_privativa", "valor_avaliacao", "ultimo_preco", "modalidade",
          "situacao", "datas_certame", "edital", "observacao"]

CAMPOS_Q = ["primeira_ausencia", "id", "cidade", "bairro", "endereco", "tipo",
            "area_privativa", "valor_avaliacao", "ultimo_preco", "modalidade",
            "situacao", "datas_certame", "edital"]


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
    ausentes = {k: antes[k] for k in antes if k not in agora}
    quarentena = ler_quarentena(a.quarentena)

    # Quem estava em quarentena e voltou a aparecer nunca saiu. Limpa sem registrar.
    voltaram = [i for i in quarentena if i in agora]
    for i in voltaram:
        del quarentena[i]

    confirmadas, novas_em_quarentena = [], []
    for i, r in ausentes.items():
        if a.quarentena and i not in quarentena:
            quarentena[i] = {c: do_portal(r, a.data).get(c, "") for c in CAMPOS_Q}
            quarentena[i]["primeira_ausencia"] = a.data
            novas_em_quarentena.append(quarentena[i])
            continue
        reg = do_portal(r, a.data)
        if i in quarentena:
            reg["observacao"] = ("saiu da lista do portal; ausente desde %s, "
                                 "confirmado em duas rodadas consecutivas; causa "
                                 "nao declarada pela fonte"
                                 % quarentena[i]["primeira_ausencia"])
            del quarentena[i]
        else:
            reg["observacao"] = ("saiu da lista do portal; causa nao declarada "
                                 "pela fonte")
        confirmadas.append(reg)

    ja = set()
    if os.path.exists(a.historico):
        with open(a.historico, encoding="utf-8-sig") as f:
            ja = {(r["data_saida"], r["id"]) for r in csv.DictReader(f, delimiter=";")}
    novas = [r for r in confirmadas if (r["data_saida"], r["id"]) not in ja]

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
