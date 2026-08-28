#!/usr/bin/env python3
"""Viabilidade de arrematação de imóvel em leilão.

Calcula o Custo Total de Aquisição (CTA), a margem líquida, o retorno
anualizado e — o entregável que vai para o certame — o lance máximo que
ainda preserva a margem-alvo.

Uso:
    python3 viabilidade.py --exemplo
    python3 viabilidade.py --json lote.json
    python3 viabilidade.py --json lote.json --formato json

Campos aceitos no JSON (todos opcionais, exceto `lance` e a origem do VVR):

    identificacao        str    rótulo do lote
    lance                float  valor pretendido de arrematação
    valor_avaliacao      float  avaliação do edital (checagem de preço vil)
    area_m2              float
    comissao_pct         float  comissão do leiloeiro        (padrão 5.0)
    itbi_pct             float                               (padrão 3.0)
    registro_pct         float  registro + escritura         (padrão 1.2)
    debito_iptu          float
    debito_condominio    float
    debito_consumo       float
    custo_desocupacao    float
    reforma              float  valor fechado de reforma
    reforma_por_m2       float  alternativa: usado se `reforma` ausente
    regularizacao        float
    carrego_mensal       float  IPTU+condomínio+consumo por mês
    meses_ciclo          float  arrematação -> venda            (padrão 9)
    custo_capital_aa     float  custo de oportunidade % a.a.    (padrão 0)
    vvr                  float  valor de venda rápida
    comparaveis          list   alternativa: preços de anúncios comparáveis
    fator_desagio        float  aplicado sobre a mediana        (padrão 0.88)
    custo_venda_pct      float  corretagem na saída             (padrão 6.0)
    margem_alvo_pct      float  margem líquida exigida          (padrão 25.0)
    aluguel_mensal       float  opcional, para cap rate
"""

import argparse
import json
import statistics
import sys

PADROES = {
    "comissao_pct": 5.0,
    "itbi_pct": 3.0,
    "registro_pct": 1.2,
    "meses_ciclo": 9.0,
    "custo_capital_aa": 0.0,
    "fator_desagio": 0.88,
    "custo_venda_pct": 6.0,
    "margem_alvo_pct": 25.0,
}

EXEMPLO = {
    "identificacao": "Apto 62 m2 - exemplo: aparenta 44% de desconto sobre a avaliacao e mesmo assim nao fecha",
    "lance": 180000.0,
    "valor_avaliacao": 320000.0,
    "area_m2": 62.0,
    "debito_iptu": 4200.0,
    "debito_condominio": 11000.0,
    "debito_consumo": 800.0,
    "custo_desocupacao": 12000.0,
    "reforma_por_m2": 700.0,
    "carrego_mensal": 950.0,
    "meses_ciclo": 10.0,
    "custo_capital_aa": 11.0,
    "comparaveis": [305000.0, 318000.0, 330000.0, 295000.0, 340000.0],
    "aluguel_mensal": 1800.0,
}


def _num(dados, chave, padrao=0.0):
    valor = dados.get(chave, PADROES.get(chave, padrao))
    if valor is None:
        valor = PADROES.get(chave, padrao)
    return float(valor)


def calcular(dados):
    lance = _num(dados, "lance")
    if lance <= 0:
        raise ValueError("informe um `lance` positivo")

    comissao_pct = _num(dados, "comissao_pct")
    itbi_pct = _num(dados, "itbi_pct")
    registro_pct = _num(dados, "registro_pct")
    meses = _num(dados, "meses_ciclo")
    capital_aa = _num(dados, "custo_capital_aa")
    custo_venda_pct = _num(dados, "custo_venda_pct")
    margem_alvo = _num(dados, "margem_alvo_pct") / 100.0

    # VVR: explícito ou derivado dos comparáveis.
    vvr = dados.get("vvr")
    comparaveis = dados.get("comparaveis") or []
    if vvr:
        vvr = float(vvr)
        mediana = None
    elif comparaveis:
        mediana = statistics.median(float(c) for c in comparaveis)
        vvr = mediana * _num(dados, "fator_desagio")
    else:
        raise ValueError("informe `vvr` ou uma lista `comparaveis`")

    reforma = dados.get("reforma")
    if reforma is None:
        reforma = _num(dados, "reforma_por_m2") * _num(dados, "area_m2")
    reforma = float(reforma)

    # Percentuais que incidem sobre o lance.
    k = (comissao_pct + itbi_pct + registro_pct) / 100.0

    debitos = (
        _num(dados, "debito_iptu")
        + _num(dados, "debito_condominio")
        + _num(dados, "debito_consumo")
    )
    carrego = _num(dados, "carrego_mensal") * meses
    fixos = (
        debitos
        + _num(dados, "custo_desocupacao")
        + reforma
        + _num(dados, "regularizacao")
        + carrego
    )

    # Custo de capital incide sobre o desembolso, proporcional ao ciclo.
    fator_capital = (capital_aa / 100.0) * (meses / 12.0)

    cta_base = lance * (1 + k) + fixos
    custo_capital = cta_base * fator_capital
    cta = cta_base + custo_capital

    receita_liquida = vvr * (1 - custo_venda_pct / 100.0)
    lucro = receita_liquida - cta
    margem = lucro / cta if cta else 0.0
    anualizado = ((1 + margem) ** (12.0 / meses) - 1) if meses > 0 else margem
    desconto_real = 1 - cta / vvr if vvr else 0.0

    # Lance máximo que ainda entrega a margem-alvo.
    cta_max = receita_liquida / (1 + margem_alvo)
    lance_max = (cta_max / (1 + fator_capital) - fixos) / (1 + k)

    aluguel = _num(dados, "aluguel_mensal")
    cap_rate = (aluguel * 12 / cta) if (aluguel and cta) else None

    avaliacao = _num(dados, "valor_avaliacao")
    perc_avaliacao = (lance / avaliacao) if avaliacao else None

    return {
        "identificacao": dados.get("identificacao", "lote sem identificacao"),
        "lance": lance,
        "composicao": {
            "lance": lance,
            "comissao_leiloeiro": lance * comissao_pct / 100.0,
            "itbi": lance * itbi_pct / 100.0,
            "registro_escritura": lance * registro_pct / 100.0,
            "debitos_assumidos": debitos,
            "desocupacao": _num(dados, "custo_desocupacao"),
            "reforma": reforma,
            "regularizacao": _num(dados, "regularizacao"),
            "carrego": carrego,
            "custo_capital": custo_capital,
        },
        "cta": cta,
        "vvr": vvr,
        "mediana_comparaveis": mediana,
        "receita_liquida": receita_liquida,
        "lucro": lucro,
        "margem_liquida": margem,
        "retorno_anualizado": anualizado,
        "desconto_real": desconto_real,
        "lance_maximo": lance_max,
        "folga_do_lance": lance_max - lance,
        "cap_rate": cap_rate,
        "perc_da_avaliacao": perc_avaliacao,
        "margem_alvo": margem_alvo,
        "meses_ciclo": meses,
    }


def alertas(r):
    saida = []
    if r["margem_liquida"] < r["margem_alvo"]:
        saida.append(
            "Margem abaixo do alvo: {:.1f}% contra {:.1f}% exigidos. "
            "O lance precisa cair para no maximo {}.".format(
                r["margem_liquida"] * 100, r["margem_alvo"] * 100,
                brl(r["lance_maximo"]))
        )
    if r["lance_maximo"] < 0:
        saida.append(
            "Nenhum lance viabiliza este lote: so os custos fixos ja consomem "
            "a receita liquida projetada."
        )
    p = r["perc_da_avaliacao"]
    if p is not None and p < 0.5:
        saida.append(
            "Lance em {:.0f}% da avaliacao — abaixo dos 50% caracterizados como "
            "preco vil. Risco relevante de anulacao da arrematacao (CPC art. 891 "
            "e jurisprudencia recente do STJ para leilao extrajudicial).".format(p * 100)
        )
    debitos = r["composicao"]["debitos_assumidos"]
    if debitos > 0.15 * r["cta"]:
        saida.append(
            "Debitos assumidos representam {:.0f}% do CTA — confirme por escrito "
            "com prefeitura e administradora antes do certame.".format(
                debitos / r["cta"] * 100)
        )
    if r["desconto_real"] < 0.20:
        saida.append(
            "Desconto real de apenas {:.0f}% sobre o VVR. Abaixo de 20% o leilao "
            "nao paga o risco.".format(r["desconto_real"] * 100)
        )
    if r["mediana_comparaveis"] is None and r["vvr"]:
        saida.append(
            "VVR informado diretamente: confirme que veio de comparaveis reais, "
            "e nao da avaliacao do edital."
        )
    if r["cap_rate"] is not None and r["cap_rate"] < 0.06:
        saida.append(
            "Cap rate de {:.1f}% a.a. — tese de renda nao fecha.".format(
                r["cap_rate"] * 100)
        )
    return saida


def brl(v):
    return "R$ {:,.2f}".format(v).replace(",", "@").replace(".", ",").replace("@", ".")


def imprimir(r):
    print()
    print("=" * 68)
    print(r["identificacao"])
    print("=" * 68)
    print("\nComposicao do Custo Total de Aquisicao")
    print("-" * 68)
    for rotulo, valor in r["composicao"].items():
        if valor:
            print("  {:<26} {:>20}".format(rotulo.replace("_", " "), brl(valor)))
    print("-" * 68)
    print("  {:<26} {:>20}".format("CTA", brl(r["cta"])))
    print()
    print("Saida")
    print("-" * 68)
    if r["mediana_comparaveis"]:
        print("  {:<26} {:>20}".format("mediana comparaveis", brl(r["mediana_comparaveis"])))
    print("  {:<26} {:>20}".format("VVR", brl(r["vvr"])))
    print("  {:<26} {:>20}".format("receita liq. de venda", brl(r["receita_liquida"])))
    print("  {:<26} {:>20}".format("lucro projetado", brl(r["lucro"])))
    print()
    print("Indicadores")
    print("-" * 68)
    print("  {:<26} {:>19.1f}%".format("margem liquida", r["margem_liquida"] * 100))
    print("  {:<26} {:>19.1f}%".format("retorno anualizado", r["retorno_anualizado"] * 100))
    print("  {:<26} {:>19.1f}%".format("desconto real s/ VVR", r["desconto_real"] * 100))
    if r["perc_da_avaliacao"] is not None:
        print("  {:<26} {:>19.1f}%".format("lance / avaliacao", r["perc_da_avaliacao"] * 100))
    if r["cap_rate"] is not None:
        print("  {:<26} {:>19.1f}%".format("cap rate a.a.", r["cap_rate"] * 100))
    print("  {:<26} {:>19.0f}".format("meses do ciclo", r["meses_ciclo"]))
    print()
    print("LANCE MAXIMO (margem alvo de {:.0f}%): {}".format(
        r["margem_alvo"] * 100, brl(r["lance_maximo"])))
    print("  folga sobre o lance simulado: {}".format(brl(r["folga_do_lance"])))
    avisos = alertas(r)
    if avisos:
        print()
        print("Alertas")
        print("-" * 68)
        for a in avisos:
            print("  ! " + a)
    print()


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--json", help="arquivo JSON com os dados do lote")
    p.add_argument("--exemplo", action="store_true", help="roda com dados de exemplo")
    p.add_argument("--formato", choices=["texto", "json"], default="texto")
    args = p.parse_args()

    if args.exemplo:
        dados = EXEMPLO
    elif args.json:
        with open(args.json, encoding="utf-8") as f:
            dados = json.load(f)
    else:
        dados = json.load(sys.stdin)

    lotes = dados if isinstance(dados, list) else [dados]
    resultados = [calcular(d) for d in lotes]

    if args.formato == "json":
        for r in resultados:
            r["alertas"] = alertas(r)
        print(json.dumps(resultados, indent=2, ensure_ascii=False))
    else:
        for r in resultados:
            imprimir(r)
        if len(resultados) > 1:
            print("Ranking por margem liquida")
            print("-" * 68)
            for r in sorted(resultados, key=lambda x: -x["margem_liquida"]):
                print("  {:>7.1f}%  {}".format(r["margem_liquida"] * 100, r["identificacao"]))
            print()


if __name__ == "__main__":
    main()
