#!/usr/bin/env python3
"""Mede os degraus de preco de lotes que PERMANECEM na lista.

    python3 degraus.py --dados dados --saida dados/degraus-preco.csv

Nasceu em 23/11/2026, quando o lote 000001028634-4 (comercial no Estreito,
Florianopolis, Venda Online) baixou exatamente 2,50% depois de sessenta dias
com o preco inalterado -- o primeiro corte de preco jamais observado em lote
que nao saiu da lista nem trocou de modalidade.

A distincao e' o ponto todo. As quedas grandes ja registradas (-22,67% e
-63,13%) sao de REOFERTA: o lote sai, perde o certame e volta com outra
referencia de preco. O degrau que este script mede e' outra coisa -- o
vendedor reduz o preco do lote que continua anunciado. Confundir os dois
superestimaria em muito o desconto que a espera produz.

Por isso o script so conta variacao entre duas coletas CONSECUTIVAS em que o
lote esta presente nas duas e a modalidade nao mudou. Qualquer coisa fora
disso e' reoferta e pertence ao retornos.csv, nao aqui.
"""
import argparse, csv, glob, os, re, sys


def num(t):
    try:
        return float(str(t or "0").replace(".", "").replace(",", "."))
    except ValueError:
        return 0.0


def coletas(pasta):
    """Devolve (ordem, rotulo, {id: linha}) de cada coleta, em ordem de tempo."""
    saida = []
    for p in glob.glob(os.path.join(pasta, "caixa-lotes-*.csv")):
        m = re.search(r"(\d{4})-(\d{2})-(\d{2})(?:-(\d{2})h)?", os.path.basename(p))
        if not m:
            continue
        hora = m.group(4) or "00"
        ordem = "%s-%s-%s-%s" % (m.group(1), m.group(2), m.group(3), hora)
        rotulo = "%s/%s/%s %sh" % (m.group(3), m.group(2), m.group(1), hora)
        with open(p, encoding="utf-8") as f:
            linhas = {r["Numero do imovel"]: r for r in csv.DictReader(f, delimiter=";")}
        saida.append((ordem, rotulo, linhas))
    saida.sort()
    return saida


def dias(o1, o2):
    """Diferenca em dias entre dois rotulos de ordem AAAA-MM-DD-HH."""
    import datetime
    f = "%Y-%m-%d-%H"
    return (datetime.datetime.strptime(o2, f) - datetime.datetime.strptime(o1, f)).days


def degraus(cs):
    """Degraus de preco em lote presente e de mesma modalidade nas duas coletas."""
    achados = []
    for (o1, r1, a), (o2, r2, b) in zip(cs, cs[1:]):
        for lote in set(a) & set(b):
            p1, p2 = num(a[lote]["Preco"]), num(b[lote]["Preco"])
            if abs(p2 - p1) <= 0.005:
                continue
            if (a[lote].get("Modalidade") or "") != (b[lote].get("Modalidade") or ""):
                continue            # reoferta: e' do retornos.csv
            av = num(b[lote]["Valor de avaliacao"])
            achados.append({
                "de": r1, "para": r2, "ordem_de": o1, "ordem_para": o2,
                "id": lote, "cidade": b[lote].get("Cidade", ""),
                "bairro": b[lote].get("Bairro", ""),
                "modalidade": b[lote].get("Modalidade", ""),
                "preco_antes": p1, "preco_depois": p2,
                "variacao_pct": (p2 / p1 - 1) * 100 if p1 else 0.0,
                "fator_antes": p1 / av if av else 0.0,
                "fator_depois": p2 / av if av else 0.0,
            })
    return achados


def estabilidade(cs, lote, ate):
    """Quantos dias o lote manteve o preco anterior, antes do degrau em `ate`."""
    visto = [(o, num(l[lote]["Preco"])) for o, _, l in cs if lote in l and o < ate]
    if not visto:
        return 0
    ultimo = visto[-1][1]
    inicio = visto[-1][0]
    for o, p in reversed(visto):
        if abs(p - ultimo) > 0.005:
            break
        inicio = o
    return dias(inicio, ate)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dados", default="dados")
    ap.add_argument("--saida", default="dados/degraus-preco.csv")
    a = ap.parse_args()

    cs = coletas(a.dados)
    if len(cs) < 2:
        print("coletas insuficientes para comparar", file=sys.stderr)
        return 1
    achados = degraus(cs)
    for d in achados:
        d["dias_no_preco_anterior"] = estabilidade(cs, d["id"], d["ordem_para"])

    campos = ["de", "para", "id", "cidade", "bairro", "modalidade", "preco_antes",
              "preco_depois", "variacao_pct", "fator_antes", "fator_depois",
              "dias_no_preco_anterior"]
    with open(a.saida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos, delimiter=";", extrasaction="ignore")
        w.writeheader()
        for d in achados:
            w.writerow(d)

    print("%d coleta(s) comparada(s) | %d degrau(s) de preco em lote que permaneceu"
          % (len(cs), len(achados)))
    for d in achados:
        print("  %s  %s/%s  %s" % (d["id"], d["cidade"], d["bairro"], d["modalidade"]))
        print("     %s -> %s: R$ %.2f -> R$ %.2f  %+.2f%%  (parado havia %d dias)"
              % (d["de"], d["para"], d["preco_antes"], d["preco_depois"],
                 d["variacao_pct"], d["dias_no_preco_anterior"]))
    if not achados:
        print("  nenhum: todo lote que permaneceu manteve o preco")
    print("gravado %s" % a.saida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
