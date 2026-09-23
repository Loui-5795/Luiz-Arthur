#!/usr/bin/env python3
"""Confere as formulas gravadas no .xlsx sem depender do LibreOffice.

    python3 conferir_planilha.py planilhas/varredura-AAAA-MM-DD-HHh.xlsx

Le as formulas como estao dentro do arquivo, resolve as referencias de celula
e avalia cada uma. Independe de como a planilha foi gerada: trabalha sobre o
que sera entregue.

O recalculo canonico seria o LibreOffice; onde ele nao carrega nem um arquivo
trivial, esta conferencia e' o que ha. Nao substitui abrir no Excel.
"""
import re, sys
from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string

REF_PREM = re.compile(r"Premissas!\$([A-Z]+)\$(\d+)")
REF_LOCAL = re.compile(r"(?<![A-Z!$])\$?([A-Z]{1,2})\$?(\d+)\b")
COL = {"VVR": 7, "CTA": 15, "margem": 18,
       "lance_max_margem": 19, "lance_max_caixa": 20}


def main(caminho):
    wb = load_workbook(caminho)
    prem, viab = wb["Premissas"], wb["Aprovados na triagem"]
    cache = {}

    def valor(ws, col, row, pilha=()):
        chave = (ws.title, col, row)
        if chave in cache:
            return cache[chave]
        if chave in pilha:
            raise RuntimeError("referencia circular em %s" % (chave,))
        v = ws.cell(row=row, column=col).value
        if isinstance(v, str) and v.startswith("="):
            v = avaliar(v[1:], ws, pilha + (chave,))
        if not isinstance(v, (int, float)):
            v = 0.0
        cache[chave] = v
        return v

    def avaliar(expr, ws, pilha):
        expr = re.sub(r"IFERROR\((.*?),\s*0\)", r"(\1)", expr)
        expr = REF_PREM.sub(lambda m: repr(float(valor(
            prem, column_index_from_string(m.group(1)), int(m.group(2)), pilha))), expr)
        if expr.startswith("IF("):
            return 0.0                      # condicional: nao entra na conferencia
        expr = REF_LOCAL.sub(lambda m: repr(float(valor(
            ws, column_index_from_string(m.group(1)), int(m.group(2)), pilha))), expr)
        return eval(expr)                   # so' aritmetica, apos as substituicoes

    erros = 0
    for row in range(5, viab.max_row + 1):
        ident = viab.cell(row=row, column=1).value
        if not ident:
            continue
        print("\n%s" % ident)
        for nome, col in COL.items():
            try:
                v = valor(viab, col, row)
                print("   %-18s %15.2f" % (nome, v))
            except Exception as e:                       # noqa: BLE001
                erros += 1
                print("   %-18s ERRO: %s" % (nome, e))
        print("   %-18s %s" % ("veredicto", viab.cell(row=row, column=22).value))

    print("\n%d celulas avaliadas | %d erro(s)" % (len(cache), erros))
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
