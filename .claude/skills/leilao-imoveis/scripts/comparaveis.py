#!/usr/bin/env python3
"""Coleta comparaveis de mercado (anuncios ativos) para montar o VVR.

    python3 comparaveis.py --cidade palhoca --bairro bela-vista \
        --saida dados/comparaveis-bela-vista-AAAA-MM-DD.csv

Busca anuncios de apartamento e casa no bairro, le a ficha de cada um para
pegar area privativa e condominio, e imprime as medianas -- inclusive a de
R$/m2 na banda de area que interessa, que e' o numero que entra no VVR.

Anuncio e' preco pedido, nao preco fechado. O fator de desagio do mandato
existe justamente por isso.
"""
import argparse, csv, json, re, statistics, subprocess, sys, time

BASE = "https://www.imoveis-sc.com.br"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def baixar(url, tentativas=3):
    for n in range(tentativas):
        r = subprocess.run(["curl", "-sS", "--max-time", "45",
                            "-H", "User-Agent: " + UA,
                            "-H", "Accept-Language: pt-BR,pt;q=0.9", url],
                           capture_output=True)
        t = r.stdout.decode("utf-8", "replace")
        if len(t) > 2000:
            return t
        time.sleep(2 * (n + 1))
    return ""


def itens(html):
    """Le a ItemList schema.org que o portal embute na pagina de resultados."""
    out = []
    for m in re.finditer(
            r'(\{"@context":"https://schema\.org","@type":"ItemList".*?\})</script>',
            html, re.S):
        try:
            d = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        for li in d.get("itemListElement", []):
            it = li.get("item", {})
            url = it.get("url") or li.get("url", "")
            mq = re.search(r"(\d+)-quartos?", url)      # o slug traz os quartos
            out.append({
                "url": url,
                "preco": float(it.get("offers", {}).get("price", 0) or 0),
                "quartos": mq.group(1) if mq else "",
                "tipo": it.get("model", ""), "sku": it.get("sku", ""),
                "anunciante": it.get("brand", {}).get("name", ""),
            })
    return out


def listar(base, paginas):
    vistos, tudo = set(), []
    for p in range(1, paginas + 1):
        url = base if p == 1 else "%s?page=%d" % (base, p)
        for r in itens(baixar(url)):
            if r["sku"] and r["sku"] not in vistos and r["preco"] > 0:
                vistos.add(r["sku"]); tudo.append(r)
        time.sleep(0.6)
    return tudo


def detalhar(registros):
    """Abre a ficha de cada anuncio: a lista nem sempre declara a area."""
    for i, r in enumerate(registros, 1):
        h = baixar(r["url"])
        r["area"] = r["condominio"] = None
        for pat in (r"(\d+[.,]?\d*)\s*m²?\s*(?:de\s*)?(?:área\s*)?privativa",
                    r"Área privativa[^0-9]{0,30}(\d+[.,]?\d*)",
                    r"Área útil[^0-9]{0,30}(\d+[.,]?\d*)",
                    r'"floorSize"[^0-9]{0,30}(\d+[.,]?\d*)',
                    r"(\d+[.,]?\d*)\s*m²"):
            m = re.search(pat, h, re.I)
            if m:
                try:
                    v = float(m.group(1).replace(",", "."))
                except ValueError:
                    continue
                if 20 <= v <= 400:
                    r["area"] = v; break
        mc = re.search(r"[Cc]ondom[íi]nio[^0-9R]{0,20}R\$\s*([\d.]+)", h)
        if mc:
            try:
                r["condominio"] = float(mc.group(1).replace(".", ""))
            except ValueError:
                pass
        print("  [%d/%d] R$ %-11.0f area=%-7s cond=%s" % (
            i, len(registros), r["preco"], r["area"], r["condominio"]),
            file=sys.stderr)
        time.sleep(0.4)
    return registros


def mediana(vals):
    return statistics.median(vals) if vals else None


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--cidade", default="palhoca")
    p.add_argument("--bairro", default="bela-vista")
    p.add_argument("--paginas", type=int, default=4)
    p.add_argument("--banda", default="42-49",
                   help="faixa de area em m2 que forma o R$/m2 do VVR")
    p.add_argument("--saida", required=True)
    a = p.parse_args()

    raiz = "%s/%s/comprar" % (BASE, a.cidade)
    aptos = detalhar(listar("%s/apartamento/%s" % (raiz, a.bairro), a.paginas))
    casas = listar("%s/casa/%s" % (raiz, a.bairro), a.paginas)
    for c in casas:
        c.setdefault("area", None); c.setdefault("condominio", None)

    lo, hi = (float(x) for x in a.banda.split("-"))
    dois = [r for r in aptos if r["quartos"] == "2"]
    banda = [r for r in dois if r["area"] and lo <= r["area"] <= hi]

    print("\n=== %s, %s — anuncios ativos ===" % (a.bairro, a.cidade), file=sys.stderr)
    resumo = {
        "n_apto_2d": len(dois),
        "mediana_apto_2d": mediana([r["preco"] for r in dois]),
        "area_mediana_2d": mediana([r["area"] for r in dois if r["area"]]),
        "n_banda": len(banda), "banda": a.banda,
        "mediana_banda": mediana([r["preco"] for r in banda]),
        "m2_mediano_banda": mediana([r["preco"] / r["area"] for r in banda]),
        "condominio_mediano": mediana([r["condominio"] for r in dois if r["condominio"]]),
        "n_casa": len(casas), "mediana_casa": mediana([r["preco"] for r in casas]),
        "n_apto_3d": len([r for r in aptos if r["quartos"] == "3"]),
    }
    for k, v in resumo.items():
        print("  %-22s %s" % (k, ("%.0f" % v) if isinstance(v, float) else v),
              file=sys.stderr)
    if resumo["n_banda"] < 5:
        print("\n  ATENCAO: menos de 5 comparaveis na banda. R$/m2 pouco confiavel.",
              file=sys.stderr)

    with open(a.saida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["grupo", "tipo", "quartos", "area",
                                          "preco", "condominio", "anunciante", "url"],
                           delimiter=";")
        w.writeheader()
        for grupo, lista in (("venda_apto", aptos), ("venda_casa", casas)):
            for r in lista:
                w.writerow({"grupo": grupo, "tipo": r["tipo"], "quartos": r["quartos"],
                            "area": r["area"], "preco": r["preco"],
                            "condominio": r["condominio"],
                            "anunciante": r["anunciante"], "url": r["url"]})
    json.dump(resumo, open(a.saida.replace(".csv", "-resumo.json"), "w"), indent=2)
    print("\ngravado %s (%d anuncios)" % (a.saida, len(aptos) + len(casas)), file=sys.stderr)


if __name__ == "__main__":
    main()
