#!/usr/bin/env python3
"""Registra os lotes que sairam da lista do portal entre duas coletas.

    python3 historico.py --anterior dados/lotes-A.csv --atual dados/lotes-B.csv \
                         --historico dados/historico-saidas.csv --data 19/09/2026

O triagem.py reescreve o pipeline.csv a cada rodada a partir da lista corrente,
entao lote que sai do portal desaparece do historico. E justamente esse o dado
que calibra lance futuro: quantos lotes da praca sumiram, de que faixa de preco
e depois de qual data de certame. Este script preserva isso, sem apagar nada.

O portal nao diz se o lote saiu por arremate, suspensao ou retirada. O registro
guarda o fato observado -- saiu da lista -- e nunca supoe a causa.
"""
import argparse, csv, os

CAMPOS = ["data_saida", "id", "cidade", "bairro", "endereco", "tipo",
          "area_privativa", "valor_avaliacao", "ultimo_preco", "modalidade",
          "situacao", "datas_certame", "edital", "observacao"]


def ler(caminho):
    with open(caminho, encoding="utf-8-sig") as f:
        return {r["Numero do imovel"]: r for r in csv.DictReader(f, delimiter=";")}


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--anterior", required=True)
    p.add_argument("--atual", required=True)
    p.add_argument("--historico", required=True)
    p.add_argument("--data", required=True)
    a = p.parse_args()

    antes, agora = ler(a.anterior), ler(a.atual)
    sairam = [antes[k] for k in antes if k not in agora]

    ja = set()
    if os.path.exists(a.historico):
        with open(a.historico, encoding="utf-8-sig") as f:
            ja = {(r["data_saida"], r["id"]) for r in csv.DictReader(f, delimiter=";")}

    novas = []
    for r in sairam:
        chave = (a.data, r["Numero do imovel"])
        if chave in ja:
            continue
        novas.append({
            "data_saida": a.data, "id": r["Numero do imovel"],
            "cidade": r.get("Cidade", ""), "bairro": r.get("Bairro", ""),
            "endereco": r.get("Endereco", ""), "tipo": r.get("Tipo", ""),
            "area_privativa": r.get("Area privativa", ""),
            "valor_avaliacao": r.get("Valor de avaliacao", ""),
            "ultimo_preco": r.get("Preco", ""), "modalidade": r.get("Modalidade", ""),
            "situacao": r.get("Situacao", ""), "datas_certame": r.get("Data certame", ""),
            "edital": r.get("Edital", ""),
            "observacao": "saiu da lista do portal; causa nao declarada pela fonte",
        })

    existe = os.path.exists(a.historico)
    with open(a.historico, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS, delimiter=";")
        if not existe:
            w.writeheader()
        w.writerows(novas)
    print("%d lote(s) sairam da lista | %d registro(s) novo(s) em %s" % (
        len(sairam), len(novas), a.historico))
    for r in novas:
        print("  %s  %-16s %-18s %-13s R$ %s" % (
            r["data_saida"], r["id"], r["bairro"][:18], r["cidade"], r["ultimo_preco"]))


if __name__ == "__main__":
    main()
