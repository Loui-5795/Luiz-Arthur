#!/usr/bin/env python3
"""Monta a planilha .xlsx da varredura.

    python3 planilha.py --lotes dados/lotes.csv --comparaveis dados/comp.csv \
                        --pipeline pipeline.csv --saida varredura.xlsx

A aba Premissas concentra todo input. As abas de viabilidade calculam por
formula referenciando aquelas celulas, entao mudar uma premissa recalcula a
margem e o lance maximo de todos os lotes -- sem rodar script nenhum.
"""
import argparse, csv, datetime, re, sys

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

FONTE = "Arial"
AZUL = Font(name=FONTE, size=10, color="0000FF")          # input digitado
PRETO = Font(name=FONTE, size=10)                          # formula
VERDE = Font(name=FONTE, size=10, color="008000")          # link entre abas
TITULO = Font(name=FONTE, size=14, bold=True)
CABEC = Font(name=FONTE, size=10, bold=True, color="FFFFFF")
FILL_CABEC = PatternFill("solid", fgColor="1F3864")
FILL_INPUT = PatternFill("solid", fgColor="FFFF00")
FILL_ALERTA = PatternFill("solid", fgColor="FFC7CE")
FILL_OK = PatternFill("solid", fgColor="C6EFCE")
BORDA = Border(*[Side(style="thin", color="BFBFBF")] * 4)

MOEDA = 'R$ #,##0;(R$ #,##0);-'
PCT = '0.0%'
M2 = '#,##0.00 "m²"'


def num(t):
    if t is None or t == "":
        return 0.0
    t = str(t)
    # "45,61m2" -> o 2 da unidade entrava no numero. Corta a unidade primeiro.
    t = re.sub(r"\s*m\s*[²2]\s*$", "", t, flags=re.IGNORECASE)
    t = re.sub(r"[^\d,.-]", "", t)
    if "," in t and "." in t:
        t = t.replace(".", "").replace(",", ".")
    elif "," in t:
        t = t.replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return 0.0


def ler(caminho):
    if not caminho:
        return []
    with open(caminho, encoding="utf-8-sig") as f:
        amostra = f.read(4096); f.seek(0)
        delim = ";" if amostra.count(";") >= amostra.count(",") else ","
        return list(csv.DictReader(f, delimiter=delim))


def cabecalho(ws, linha, titulos, larguras=None):
    for i, t in enumerate(titulos, 1):
        c = ws.cell(row=linha, column=i, value=t)
        c.font = CABEC; c.fill = FILL_CABEC; c.border = BORDA
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    if larguras:
        for i, w in enumerate(larguras, 1):
            ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = ws.cell(row=linha + 1, column=1)


# --------------------------------------------------------------- Premissas
PREMISSAS = [
    ("Custos sobre o lance", None, None, None),
    ("Comissão do leiloeiro", 0.05, PCT, "Edital do lote. 5% é o padrão da Caixa, mas confira."),
    ("ITBI", 0.03, PCT, "Palhoça: faixa de 2% a 3%. Confirmar na Prefeitura."),
    ("Registro e escritura", 0.012, PCT, "Tabela de emolumentos de SC."),
    ("Dívidas e custos fixos", None, None, None),
    ("IPTU atrasado", 3000.0, MOEDA, "Faixa R$ 1 a 5 mil. Em hasta pública sub-roga no preço (Tema 1.134 STJ)."),
    ("Condomínio atrasado", 12000.0, MOEDA, "Faixa R$ 0 a 20 mil. É o item que mais move a margem — peça por escrito à administradora."),
    ("Contas de consumo", 800.0, MOEDA, "Água e luz em atraso."),
    ("Desocupação", 15000.0, MOEDA, "Acordo: R$ 5 a 25 mil. Litigiosa: R$ 10 a 40 mil e 12 a 36 meses."),
    ("Reforma por m²", 550.0, MOEDA, "Leve: R$ 400 a 700/m². Pesada: R$ 900 a 1.800/m². Sem vistoria é estimativa."),
    ("Carrego mensal", 560.0, MOEDA, "Condomínio mediano do bairro (R$ 400) + IPTU + consumo."),
    ("Meses do ciclo", 12.0, '0', "Arrematação até a venda. O perfil aceita 6 a 12 meses."),
    ("Saída e mandato", None, None, None),
    ("Custo de venda (corretagem)", 0.06, PCT, "Definido no perfil-investidor.md."),
    ("Fator de deságio do VVR", 0.88, '0.00', "Venda em 90 dias. Definido no perfil-investidor.md."),
    ("Margem líquida mínima", 0.25, PCT, "Abaixo disso o perfil manda descartar."),
    ("Mercado e caixa", None, None, None),
    ("R$/m² de mercado", 5920.0, MOEDA, "Mediana de 14 anúncios de 2 dorm. entre 42 e 49 m² em Bela Vista, 16/09/2026."),
    ("Capital disponível", 100000.0, MOEDA, "Perfil: R$ 50.000 a R$ 100.000. Aqui no topo da faixa."),
    ("% do lance pago à vista", 1.0, PCT, "100% = sem financiamento. Nenhum lote de Palhoça aceita financiamento."),
]
REF = {}     # rotulo -> "Premissas!$B$n"


def aba_premissas(wb):
    ws = wb.create_sheet("Premissas")
    ws["A1"] = "Premissas da varredura"; ws["A1"].font = TITULO
    ws["A2"] = ("Só se edita esta aba. As células amarelas alimentam por fórmula todas as "
                "contas das outras abas — mude uma e a margem e o lance máximo se refazem sozinhos.")
    ws["A2"].font = Font(name=FONTE, size=9, italic=True)
    ws.column_dimensions["A"].width = 32; ws.column_dimensions["B"].width = 16
    ws.column_dimensions["C"].width = 90
    linha = 4
    for rotulo, valor, fmt, nota in PREMISSAS:
        if valor is None:                                   # subtitulo de bloco
            c = ws.cell(row=linha, column=1, value=rotulo)
            c.font = Font(name=FONTE, size=10, bold=True)
            linha += 1; continue
        ws.cell(row=linha, column=1, value=rotulo).font = PRETO
        c = ws.cell(row=linha, column=2, value=valor)
        c.font = AZUL; c.fill = FILL_INPUT; c.number_format = fmt; c.border = BORDA
        n = ws.cell(row=linha, column=3, value=nota)
        n.font = Font(name=FONTE, size=9, color="595959")
        n.alignment = Alignment(wrap_text=True, vertical="top")
        REF[rotulo] = "Premissas!$B$%d" % linha
        linha += 1
    linha += 1
    ws.cell(row=linha, column=1, value="Legenda").font = Font(name=FONTE, size=10, bold=True)
    for txt, fnt, fill in (("azul sobre amarelo = você edita", AZUL, FILL_INPUT),
                           ("preto = fórmula, não mexa", PRETO, None),
                           ("verde = vem de outra aba", VERDE, None)):
        linha += 1
        c = ws.cell(row=linha, column=1, value=txt); c.font = fnt
        if fill: c.fill = fill
    return ws


# ------------------------------------------------------------- Viabilidade
COLS = ["Nº do imóvel", "Bairro", "Endereço", "Área priv. (m²)", "Avaliação Caixa",
        "Lance (piso)", "VVR", "Comissão", "ITBI", "Registro", "Dívidas",
        "Desocupação", "Reforma", "Carrego", "CTA", "Receita líq. de venda",
        "Lucro", "Margem", "Lance máx. p/ margem", "Lance máx. p/ caixa",
        "Falta de caixa", "Veredicto", "Situação", "Modalidade", "Matrícula",
        "1º leilão", "2º leilão", "Edital", "FGTS", "Financia?", "Link"]
LARG = [16, 16, 46, 13, 14, 14, 14, 12, 12, 12, 12, 13, 12, 12, 14, 16, 13, 9,
        16, 16, 14, 26, 11, 15, 12, 12, 12, 18, 7, 10, 40]


def aba_viabilidade(wb, nome, lotes, nota):
    ws = wb.create_sheet(nome)
    ws["A1"] = nome; ws["A1"].font = TITULO
    ws["A2"] = nota; ws["A2"].font = Font(name=FONTE, size=9, italic=True)
    ws["A2"].alignment = Alignment(wrap_text=True)
    ws.row_dimensions[2].height = 28
    cabecalho(ws, 4, COLS, LARG)

    p_com, p_itbi, p_reg = REF["Comissão do leiloeiro"], REF["ITBI"], REF["Registro e escritura"]
    p_iptu, p_cond, p_cons = REF["IPTU atrasado"], REF["Condomínio atrasado"], REF["Contas de consumo"]
    p_des, p_ref, p_car = REF["Desocupação"], REF["Reforma por m²"], REF["Carrego mensal"]
    p_mes, p_venda, p_desag = REF["Meses do ciclo"], REF["Custo de venda (corretagem)"], REF["Fator de deságio do VVR"]
    p_marg, p_m2, p_cap = REF["Margem líquida mínima"], REF["R$/m² de mercado"], REF["Capital disponível"]
    p_ent = REF["% do lance pago à vista"]

    r = 5
    for lt in lotes:
        area = num(lt.get("Area privativa")) or num(lt.get("Area total"))
        lance = num(lt.get("Preco"))
        vals = [lt.get("Numero do imovel", ""), lt.get("Bairro", ""), lt.get("Endereco", ""),
                area, num(lt.get("Valor de avaliacao")), lance]
        for i, v in enumerate(vals, 1):
            c = ws.cell(row=r, column=i, value=v); c.font = PRETO; c.border = BORDA
        ws.cell(row=r, column=4).number_format = M2
        ws.cell(row=r, column=5).number_format = MOEDA
        ws.cell(row=r, column=6).number_format = MOEDA
        ws.cell(row=r, column=6).font = AZUL
        ws.cell(row=r, column=6).fill = FILL_INPUT      # o lance e' a alavanca do usuario

        # k = soma dos percentuais sobre o lance; fixos = tudo que nao varia com o lance
        k = "(%s+%s+%s)" % (p_com, p_itbi, p_reg)
        fixos = "(K{r}+L{r}+M{r}+N{r})".format(r=r)
        f = {
            7:  "=D{r}*{m2}*{des}".format(r=r, m2=p_m2, des=p_desag),
            8:  "=F{r}*{p}".format(r=r, p=p_com),
            9:  "=F{r}*{p}".format(r=r, p=p_itbi),
            10: "=F{r}*{p}".format(r=r, p=p_reg),
            11: "={a}+{b}+{c}".format(a=p_iptu, b=p_cond, c=p_cons),
            12: "=%s" % p_des,
            13: "=D{r}*{p}".format(r=r, p=p_ref),
            14: "={c}*{m}".format(c=p_car, m=p_mes),
            15: "=F{r}+H{r}+I{r}+J{r}+K{r}+L{r}+M{r}+N{r}".format(r=r),
            16: "=G{r}*(1-{p})".format(r=r, p=p_venda),
            17: "=P{r}-O{r}".format(r=r),
            18: "=IFERROR(Q{r}/O{r},0)".format(r=r),
            19: "=(P{r}/(1+{marg})-{fix})/(1+{k})".format(r=r, marg=p_marg, fix=fixos, k=k),
            20: "=IFERROR(({cap}-{fix})/({ent}+{k}),0)".format(cap=p_cap, fix=fixos, ent=p_ent, k=k),
            21: "={cap}-O{r}".format(r=r, cap=p_cap),
            22: ('=IF(U{r}<0,"Fora de alcance: falta caixa",'
                 'IF(R{r}<{marg},"Reprova: margem abaixo do mínimo","Persegue"))').format(r=r, marg=p_marg),
        }
        for col, formula in f.items():
            c = ws.cell(row=r, column=col, value=formula)
            c.font = PRETO; c.border = BORDA
            c.number_format = PCT if col == 18 else MOEDA
        ws.cell(row=r, column=22).number_format = "General"
        ws.cell(row=r, column=22).alignment = Alignment(wrap_text=True)

        resto = [lt.get("Situacao", ""), lt.get("Modalidade", ""), lt.get("Matricula", "")]
        datas = (lt.get("Data certame") or "").split(" / ")
        resto += [datas[0] if datas else "", datas[1] if len(datas) > 1 else "",
                  lt.get("Edital", ""), lt.get("Aceita FGTS", ""),
                  lt.get("Aceita financiamento", ""), lt.get("Link", "")]
        for i, v in enumerate(resto, 23):
            c = ws.cell(row=r, column=i, value=v); c.font = PRETO; c.border = BORDA
        r += 1

    if lotes:
        # realce condicional simples, resolvido na geracao
        ws.conditional_formatting  # noqa: B018  (mantem a intencao explicita)
        for linha in range(5, r):
            ws.cell(row=linha, column=22).fill = FILL_ALERTA
        ws.auto_filter.ref = "A4:%s%d" % (get_column_letter(len(COLS)), r - 1)
    return ws


# ------------------------------------------------------------------- Abas simples
def aba_tabela(wb, nome, linhas, titulo, nota, colunas=None):
    ws = wb.create_sheet(nome)
    ws["A1"] = titulo; ws["A1"].font = TITULO
    ws["A2"] = nota; ws["A2"].font = Font(name=FONTE, size=9, italic=True)
    if not linhas:
        ws["A4"] = "Nada coletado nesta rodada."; ws["A4"].font = PRETO
        return ws
    cols = colunas or list(linhas[0].keys())
    cabecalho(ws, 4, cols, [max(12, min(44, len(c) + 6)) for c in cols])
    for i, lt in enumerate(linhas, 5):
        for j, col in enumerate(cols, 1):
            v = lt.get(col, "")
            dinheiro = col in ("Preco", "Valor de avaliacao", "Preco 1o leilao",
                               "Preco 2o leilao", "preco")
            area_col = col in ("Area total", "Area privativa", "area", "area_ficha")
            pct = col == "Desconto"
            if dinheiro or area_col:
                v = num(v)
            elif pct:
                v = num(v) / 100.0
            c = ws.cell(row=i, column=j, value=v)
            c.font = PRETO; c.border = BORDA
            if dinheiro:
                c.number_format = MOEDA
            elif area_col:
                c.number_format = M2
            elif pct:
                c.number_format = PCT
    ws.auto_filter.ref = "A4:%s%d" % (get_column_letter(len(cols)), len(linhas) + 4)
    return ws


def aba_leiame(wb, data, n_total, n_aprov, n_comp):
    ws = wb.create_sheet("Leia-me", 0)
    ws.column_dimensions["A"].width = 110
    ws["A1"] = "Varredura de imóveis em leilão — %s" % data
    ws["A1"].font = TITULO
    texto = [
        "",
        "COMO USAR",
        "1. Abra a aba Premissas. Só as células amarelas se editam.",
        "2. Mude uma premissa (condomínio atrasado, desocupação, reforma) e todas as abas se refazem.",
        "3. Na aba Viabilidade, a coluna F (Lance) também é amarela: simule o lance que quiser.",
        "4. A coluna Veredicto diz se o lote passa no mandato do perfil-investidor.md.",
        "",
        "O QUE TEM NESTE ARQUIVO",
        "Aprovados na triagem — lotes dentro da praça-alvo, com a viabilidade calculada por fórmula.",
        "Todos os lotes — tudo que a varredura coletou, inclusive o que foi descartado e por quê.",
        "Comparáveis — os anúncios de mercado que formam o VVR.",
        "Premissas — os inputs.",
        "",
        "NÚMEROS DESTA RODADA",
        "Lotes coletados: %d" % n_total,
        "Aprovados na triagem: %d" % n_aprov,
        "Comparáveis de mercado: %d" % n_comp,
        "",
        "O QUE ESTE ARQUIVO NÃO É",
        "Não é laudo de avaliação nem parecer jurídico.",
        "Nenhuma matrícula foi lida. Nenhum edital foi lido integralmente. Nenhum débito foi confirmado.",
        "Nenhuma vistoria foi feita. Os comparáveis são preços pedidos em anúncio, não preços fechados.",
        "Os custos são faixas de triagem, não cotações. Antes de qualquer lance: edital integral,",
        "matrícula atualizada, débito de condomínio por escrito, e advogado.",
    ]
    for i, t in enumerate(texto, 2):
        c = ws.cell(row=i, column=1, value=t)
        c.font = Font(name=FONTE, size=10,
                      bold=t.isupper() and len(t) > 3)
        c.alignment = Alignment(wrap_text=True)
    return ws


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--lotes", required=True)
    p.add_argument("--comparaveis")
    p.add_argument("--pipeline")
    p.add_argument("--saida", required=True)
    p.add_argument("--data", default=datetime.date.today().strftime("%d/%m/%Y"))
    a = p.parse_args()

    lotes = ler(a.lotes)
    comps = ler(a.comparaveis)
    pipe = {l["id"]: l for l in ler(a.pipeline)} if a.pipeline else {}

    aprovados, descartados = [], []
    for lt in lotes:
        st = pipe.get(lt.get("Numero do imovel", ""), {})
        lt["Status triagem"] = st.get("status", "NAO TRIADO")
        lt["Motivo do descarte"] = st.get("motivo_descarte", "")
        (aprovados if lt["Status triagem"] == "TRIAGEM" else descartados).append(lt)

    wb = Workbook(); wb.remove(wb.active)
    aba_leiame(wb, a.data, len(lotes), len(aprovados), len(comps))
    aba_premissas(wb)
    aba_viabilidade(wb, "Aprovados na triagem", aprovados,
                    "Lotes dentro da praça-alvo do perfil. Amarelo = você edita. "
                    "Tudo o mais é fórmula que lê a aba Premissas.")
    cols_todos = ["Numero do imovel", "Status triagem", "Motivo do descarte", "Cidade",
                  "Bairro", "Endereco", "Tipo", "Quartos", "Garagem", "Area total",
                  "Area privativa", "Valor de avaliacao", "Preco 1o leilao",
                  "Preco 2o leilao", "Desconto", "Situacao", "Modalidade", "Matricula",
                  "Comarca", "Data certame", "Leiloeiro", "Plataforma",
                  "Formas de pagamento", "Condominio (regra)", "Tributos (regra)",
                  "Aceita FGTS", "Aceita financiamento", "Edital PDF", "Matricula PDF", "Link"]
    cols_todos = [c for c in cols_todos if not lotes or c in lotes[0]]
    aba_tabela(wb, "Todos os lotes", lotes, "Tudo que a varredura coletou",
               "Inclui os descartados, com o motivo. %d lotes." % len(lotes), cols_todos)
    aba_tabela(wb, "Comparáveis", comps, "Anúncios ativos que formam o VVR",
               "Preço pedido, não preço fechado. %d anúncios." % len(comps))

    wb.save(a.saida)
    print("planilha gravada: %s" % a.saida)
    print("  %d lotes (%d aprovados) | %d comparaveis" % (len(lotes), len(aprovados), len(comps)))


if __name__ == "__main__":
    main()
