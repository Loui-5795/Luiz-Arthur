#!/usr/bin/env python3
"""Recalcula, sobre TODAS as coletas gravadas, o que a modalidade determina.

    python3 panorama.py --dados dados --saida dados/panorama-modalidade.csv

Existe por causa de um erro. Ate 06/10/2026 a tabela "O que a modalidade
determina" do perfil-investidor.md era atualizada a mao, e por isso envelheceu:
registrava zero financiamentos em Leilao SFI quando o estoque ja trazia um. O
numero estava certo para a amostra de quando foi escrito e errado para a de
hoje -- que e' o modo mais traicoeiro de um dado estar errado, porque nao parece
desatualizado, parece apurado.

Cada lote entra UMA vez, pela primeira coleta em que apareceu. Contar por
coleta inflaria a amostra: um lote visto em vinte rodadas nao sao vinte lotes.
"""
import argparse, collections, csv, glob, os, sys


def ler_todas(pasta):
    """Lotes distintos, na primeira versao em que foram vistos."""
    vistos, arquivos = {}, sorted(glob.glob(os.path.join(pasta, "caixa-lotes-*.csv")))
    if not arquivos:
        print("Nenhuma coleta encontrada em %s" % pasta, file=sys.stderr)
        sys.exit(2)
    for p in arquivos:
        with open(p, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f, delimiter=";"):
                i = r.get("Numero do imovel")
                if i and i not in vistos:
                    r["_primeira_coleta"] = os.path.basename(p)
                    vistos[i] = r
    return vistos, arquivos


def tem_teto_condominio(r):
    """"sob responsabilidade do comprador, ate o limite de 10% do valor de
    avaliacao" -- a Caixa paga o excedente. E' o que elimina a cauda de risco."""
    return "limite" in (r.get("Condominio (regra)") or "").lower()


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dados", default="dados")
    p.add_argument("--saida")
    a = p.parse_args()

    vistos, arquivos = ler_todas(a.dados)
    por_mod = collections.defaultdict(lambda: collections.Counter())
    for r in vistos.values():
        m = r.get("Modalidade") or "(sem modalidade)"
        c = por_mod[m]
        c["lotes"] += 1
        c["teto_condominio"] += 1 if tem_teto_condominio(r) else 0
        c["financiamento"] += 1 if r.get("Aceita financiamento") == "SIM" else 0
        c["fgts"] += 1 if r.get("Aceita FGTS") == "SIM" else 0

    print("%d lotes distintos em %d coletas (%s a %s)\n" % (
        len(vistos), len(arquivos),
        os.path.basename(arquivos[0]), os.path.basename(arquivos[-1])))
    print("| Modalidade | Lotes | Teto de condomínio atrasado | Permite financiamento | Aceita FGTS |")
    print("|---|---|---|---|---|")
    linhas = []
    for m in sorted(por_mod, key=lambda k: -por_mod[k]["lotes"]):
        c = por_mod[m]
        print("| %s | %d | %d | %d | %d |" % (
            m, c["lotes"], c["teto_condominio"], c["financiamento"], c["fgts"]))
        linhas.append({"modalidade": m, "lotes": c["lotes"],
                       "teto_condominio": c["teto_condominio"],
                       "financiamento": c["financiamento"], "fgts": c["fgts"]})

    # Os casos raros interessam mais que as contagens: sao eles que derrubam regra.
    raros = [(i, r) for i, r in sorted(vistos.items())
             if r.get("Aceita financiamento") == "SIM"]
    if raros:
        print("\nLotes que aceitam financiamento (confira-se lote a lote, nunca "
              "pela modalidade):", file=sys.stderr)
        for i, r in raros:
            print("  %-16s %-14s %-18s %-12s %-14s R$ %-14s FGTS=%s" % (
                i, r.get("Cidade", ""), r.get("Bairro", ""), r.get("Tipo", ""),
                r.get("Modalidade", ""), r.get("Preco", ""),
                r.get("Aceita FGTS", "")), file=sys.stderr)

    if a.saida:
        with open(a.saida, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()), delimiter=";")
            w.writeheader(); w.writerows(linhas)
        print("\ngravado %s" % a.saida, file=sys.stderr)


if __name__ == "__main__":
    main()
