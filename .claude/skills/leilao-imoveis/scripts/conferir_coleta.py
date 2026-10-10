#!/usr/bin/env python3
"""Compara duas coletas e acusa campo que esvaziou em bloco.

    python3 conferir_coleta.py --anterior dados/caixa-lotes-A.csv \
                               --atual dados/caixa-lotes-B.csv

Existe por causa de 10/10/2026. Naquela manha, TODOS os dezessete lotes
perderam o campo "Situacao" ao mesmo tempo: a Caixa reformulou a pagina de
detalhe e deixou de publicar a ocupacao. O coletor nao reclamou, porque o
campo nao esta entre os essenciais, e a perda so foi notada porque o diff da
rodada imprimiu dezesseis linhas iguais de "Ocupado -> ''".

Dai a regra: **campo que esvazia para todos os lotes de uma vez nao e' fato do
mercado, e' mudanca na fonte.** Nenhum evento do mundo desocupa dezessete
imoveis entre as 19h e as 07h. O mesmo vale ao contrario, para o campo que
aparece de uma vez -- e' sinal de que a fonte passou a publicar algo novo, que
convem aproveitar.

Codigo de saida 1 quando ha colapso, para que a rodada pare e olhe.
"""
import argparse, csv, os, sys

# Abaixo deste preenchimento um campo e' considerado colapsado.
PISO = 0.20
# Campos que legitimamente variam muito de lote para lote: certame em branco e'
# normal na Venda Online, condominio e tributos nem sempre vem declarados.
TOLERADOS = {"Data certame", "Condominio (regra)", "Tributos (regra)",
             "Leiloeiro", "Plataforma", "Edital", "Edital PDF", "Oficio",
             "Averbacao leiloes negativos", "Inscricao imobiliaria"}


def ler(caminho):
    with open(caminho, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f, delimiter=";"))


def preenchimento(linhas, campo):
    if not linhas:
        return 0.0
    cheios = sum(1 for r in linhas if (r.get(campo) or "").strip())
    return cheios / len(linhas)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--anterior", required=True)
    p.add_argument("--atual", required=True)
    p.add_argument("--piso", type=float, default=PISO)
    a = p.parse_args()

    if not os.path.exists(a.anterior):
        print("coleta anterior inexistente (%s); nada a comparar" % a.anterior)
        return
    antes, agora = ler(a.anterior), ler(a.atual)
    campos = [c for c in (agora[0].keys() if agora else []) if c in (antes[0] if antes else {})]

    colapsos, surgimentos = [], []
    for c in campos:
        pa, pb = preenchimento(antes, c), preenchimento(agora, c)
        if pa >= 0.80 and pb < a.piso and c not in TOLERADOS:
            colapsos.append((c, pa, pb))
        elif pa < a.piso and pb >= 0.80:
            surgimentos.append((c, pa, pb))

    novos = [c for c in (agora[0].keys() if agora else []) if c not in (antes[0] if antes else {})]
    sumidos = [c for c in (antes[0] if antes else {}) if c not in (agora[0] if agora else {})]

    print("%d lote(s) antes | %d agora | %d campo(s) comparado(s)"
          % (len(antes), len(agora), len(campos)))
    if novos:
        print("  coluna(s) NOVA(s) na coleta: %s" % ", ".join(novos))
    if sumidos:
        print("  coluna(s) que SUMIRAM da coleta: %s" % ", ".join(sumidos))
    for c, pa, pb in surgimentos:
        print("  campo passou a vir preenchido: %-28s %.0f%% -> %.0f%%"
              % (c, pa * 100, pb * 100))

    if not colapsos:
        print("Nenhum campo esvaziou em bloco.")
        return

    print("\nCOLAPSO DE CAMPO — a fonte mudou, isto nao e' fato do mercado:",
          file=sys.stderr)
    for c, pa, pb in colapsos:
        print("  %-28s preenchido em %.0f%% dos lotes e agora em %.0f%%"
              % (c, pa * 100, pb * 100), file=sys.stderr)
    print("Nenhum evento do mundo muda um campo para todos os lotes de uma vez. "
          "Conferir a pagina da fonte antes de usar esta coleta.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
