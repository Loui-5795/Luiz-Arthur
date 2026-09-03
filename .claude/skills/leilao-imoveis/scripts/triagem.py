#!/usr/bin/env python3
"""Triagem de listas de imoveis de leilao (export da Caixa e similares).

Le o arquivo que o portal exporta por UF, normaliza as colunas, aplica os
criterios de corte do mandato e devolve os lotes ordenados por prioridade de
due diligence -- alem das linhas prontas para o pipeline.csv.

    python3 triagem.py lista_MG.csv --cidade "Belo Horizonte" --ate 250000
    python3 triagem.py lista_MG.csv --uf MG --desconto-min 30 --pipeline pipeline.csv
    python3 triagem.py --exemplo

O que este script NAO faz: calcular margem. Margem exige VVR, e VVR exige
comparaveis de mercado que nao estao no arquivo. A prioridade aqui diz apenas
onde vale gastar a proxima hora de pesquisa -- quem decide o lance e o
viabilidade.py, depois da due diligence.
"""

import argparse
import csv
import io
import re
import sys
import unicodedata
from datetime import date

# Cada campo interno e casado com o cabecalho do arquivo por palavras-chave.
# O export da Caixa muda de nome entre versoes; casar por conteudo aguenta isso.
MAPA = {
    "id":         ["numero do imovel", "numero", "imovel", "lote"],
    "uf":         ["uf", "estado"],
    "cidade":     ["cidade", "municipio", "localidade"],
    "bairro":     ["bairro"],
    "endereco":   ["endereco", "logradouro"],
    "preco":      ["preco", "valor minimo", "valor de venda", "valor venda", "lance minimo"],
    "avaliacao":  ["valor de avaliacao", "avaliacao"],
    "desconto":   ["desconto"],
    "descricao":  ["descricao", "observacao", "detalhes"],
    "modalidade": ["modalidade", "tipo de venda", "forma de venda"],
    "link":       ["link", "url", "endereco eletronico"],
}

MODALIDADE_RISCO = {           # nota bruta 0-10 de seguranca juridica
    "venda direta": 10, "compra direta": 10, "venda online": 9,
    "licitacao aberta": 7, "1o leilao": 5, "2o leilao": 3, "leilao sfi": 4,
}


def sem_acento(t):
    t = unicodedata.normalize("NFKD", str(t))
    return "".join(c for c in t if not unicodedata.combining(c)).lower().strip()


def abrir(caminho):
    """Le o arquivo tolerando encoding e delimitador variaveis."""
    bruto = open(caminho, "rb").read()
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            texto = bruto.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        texto = bruto.decode("latin-1", "replace")

    linhas = [l for l in texto.splitlines() if l.strip()]
    # O export costuma vir com preambulo antes do cabecalho real: procura a
    # primeira linha que parece cabecalho (tem varios campos e nomes conhecidos).
    delim = max(";,\t", key=lambda d: sum(l.count(d) for l in linhas[:40]))
    inicio = 0
    for i, l in enumerate(linhas[:40]):
        campos = [sem_acento(c) for c in l.split(delim)]
        if len(campos) >= 4 and any(
            any(p in c for p in ("preco", "cidade", "bairro", "imovel", "valor"))
            for c in campos
        ):
            inicio = i
            break
    return list(csv.DictReader(io.StringIO("\n".join(linhas[inicio:])), delimiter=delim))


def normalizar(linha):
    """Traduz uma linha do arquivo para os campos internos."""
    achado = {}
    for campo, chaves in MAPA.items():
        for col, val in linha.items():
            if col is None:
                continue
            c = sem_acento(col)
            if any(k in c for k in chaves):
                if val and str(val).strip():
                    achado[campo] = str(val).strip()
                    break
    return achado


def dinheiro(t):
    if not t:
        return 0.0
    t = re.sub(r"[^\d,.-]", "", str(t))
    if "," in t and "." in t:            # 1.234.567,89
        t = t.replace(".", "").replace(",", ".")
    elif "," in t:
        t = t.replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return 0.0


def percentual(t):
    m = re.search(r"(\d+[.,]?\d*)", str(t or ""))
    return float(m.group(1).replace(",", ".")) if m else 0.0


def ocupacao(texto):
    t = sem_acento(texto)
    if "desocupado" in t or "vazio" in t:
        return "DESOCUPADO", 10
    if "ocupado" in t:
        return "OCUPADO", 4
    return "DESCONHECIDO", 5


def nota_modalidade(texto):
    t = sem_acento(texto)
    for chave, nota in MODALIDADE_RISCO.items():
        if chave in t:
            return nota
    return 5


def avaliar(bruto, args):
    d = normalizar(bruto)
    preco = dinheiro(d.get("preco"))
    aval = dinheiro(d.get("avaliacao"))
    desc = percentual(d.get("desconto")) or (
        (1 - preco / aval) * 100 if aval and preco else 0.0)
    contexto = " ".join(str(d.get(k, "")) for k in ("descricao", "endereco", "modalidade"))
    ocup, nota_ocup = ocupacao(contexto)
    nota_mod = nota_modalidade(d.get("modalidade", "") + " " + contexto)

    cortes = []
    if args.ate and preco > args.ate:
        cortes.append("acima_do_teto")
    if args.de and preco < args.de:
        cortes.append("abaixo_do_piso")
    if desc < args.desconto_min:
        cortes.append("desconto_anunciado_baixo")
    if args.uf and sem_acento(d.get("uf", "")) != sem_acento(args.uf):
        cortes.append("fora_da_uf")
    if args.cidade and sem_acento(args.cidade) not in sem_acento(d.get("cidade", "")):
        cortes.append("fora_da_cidade")
    if args.bairros:
        alvo = [sem_acento(b) for b in args.bairros]
        if not any(b in sem_acento(d.get("bairro", "")) for b in alvo):
            cortes.append("fora_do_bairro")
    if args.so_desocupado and ocup != "DESOCUPADO":
        cortes.append("ocupacao_nao_aceita")

    # Prioridade de pesquisa: onde gastar a proxima hora. Nao e margem.
    prioridade = round(
        min(desc, 60) / 60 * 45 + nota_mod / 10 * 30 + nota_ocup / 10 * 25, 1)

    d.update(preco=preco, avaliacao=aval, desconto=round(desc, 1), ocupacao=ocup,
             prioridade=prioridade, cortes=cortes,
             status="DESCARTADO" if cortes else "TRIAGEM")
    return d


def linha_pipeline(d):
    return {
        "id": d.get("id", "NV"), "data_analise": date.today().isoformat(),
        "comitente": "CAIXA", "modalidade": d.get("modalidade", "NV"),
        "uf": d.get("uf", "NV"), "cidade": d.get("cidade", "NV"),
        "bairro": d.get("bairro", "NV"), "tipo": "NV", "area_m2": "NV",
        "matricula": "NV", "valor_avaliacao": d.get("avaliacao", 0),
        "lance_minimo": d.get("preco", 0), "vvr": "NV", "cta_no_minimo": "NV",
        "lance_maximo": "NV", "margem_projetada": "NV", "score": "NV",
        "ocupacao": d.get("ocupacao", "DESCONHECIDO"),
        "debitos_declarados": "NV", "data_certame": "NV", "plataforma": "NV",
        "link_edital": d.get("link", "NV"), "status": d["status"],
        "motivo_descarte": ";".join(d["cortes"]), "resultado": "NV",
        "valor_arrematado": "NV", "arrematante": "NV",
    }


def brl(v):
    return "R$ {:,.0f}".format(v).replace(",", ".")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("arquivo", nargs="?", help="lista exportada do portal")
    p.add_argument("--exemplo", action="store_true")
    p.add_argument("--uf")
    p.add_argument("--cidade")
    p.add_argument("--bairros", nargs="*", default=[])
    p.add_argument("--de", type=float, default=0, help="preco minimo")
    p.add_argument("--ate", type=float, default=0, help="teto de preco")
    p.add_argument("--desconto-min", type=float, default=20.0,
                   help="desconto anunciado minimo, em %% (padrao 20)")
    p.add_argument("--so-desocupado", action="store_true")
    p.add_argument("--top", type=int, default=15)
    p.add_argument("--pipeline", help="grava/atualiza o pipeline.csv neste caminho")
    args = p.parse_args()

    if args.exemplo:
        amostra = (
            "Numero do imovel;UF;Cidade;Bairro;Endereco;Preco;Valor de avaliacao;"
            "Desconto;Descricao;Modalidade\n"
            "8444712;MG;Belo Horizonte;Santa Efigenia;Rua A, 100;185.000,00;"
            "320.000,00;42,19;Apartamento, 62m2, 2 quartos. Ocupado.;2o Leilao SFI\n"
            "8444713;MG;Belo Horizonte;Buritis;Rua B, 200;295.000,00;"
            "410.000,00;28,05;Apartamento, 78m2, 3 quartos. Desocupado.;Licitacao Aberta\n"
            "8444714;MG;Contagem;Eldorado;Rua C, 300;138.000,00;150.000,00;8,00;"
            "Casa, 90m2. Desocupado.;Venda Direta\n"
            "8444715;MG;Belo Horizonte;Barreiro;Rua D, 400;96.000,00;198.000,00;"
            "51,52;Apartamento, 48m2. Desocupado.;Venda Online\n"
        )
        caminho = "/tmp/exemplo_lista.csv"
        open(caminho, "w", encoding="utf-8").write(amostra)
        args.arquivo, args.uf = caminho, "MG"
    if not args.arquivo:
        p.error("informe o arquivo da lista ou use --exemplo")

    lotes = [avaliar(l, args) for l in abrir(args.arquivo)]
    aprovados = sorted([d for d in lotes if not d["cortes"]],
                       key=lambda d: -d["prioridade"])
    descartados = [d for d in lotes if d["cortes"]]

    print("\nLidos {} lotes | {} passaram na triagem | {} descartados\n".format(
        len(lotes), len(aprovados), len(descartados)))
    if aprovados:
        print("{:<5} {:<10} {:>7} {:>12} {:>7} {:<13} {:<22}".format(
            "PRIO", "ID", "DESC%", "PRECO", "OCUP", "MODALIDADE", "BAIRRO"))
        print("-" * 82)
        for d in aprovados[:args.top]:
            print("{:<5.1f} {:<10} {:>6.1f}% {:>12} {:>7} {:<13} {:<22}".format(
                d["prioridade"], str(d.get("id", "?"))[:10], d["desconto"],
                brl(d["preco"]), d["ocupacao"][:7],
                str(d.get("modalidade", ""))[:13], str(d.get("bairro", ""))[:22]))
    if descartados:
        motivos = {}
        for d in descartados:
            for c in d["cortes"]:
                motivos[c] = motivos.get(c, 0) + 1
        print("\nDescartes: " + " | ".join(
            "{} {}".format(v, k) for k, v in sorted(motivos.items(), key=lambda x: -x[1])))

    print("\nProximo passo: due diligence dos {} primeiros (matricula, edital, "
          "debitos), depois viabilidade.py com os comparaveis de mercado.\n".format(
              min(args.top, len(aprovados))))

    if args.pipeline:
        linhas = [linha_pipeline(d) for d in lotes]
        with open(args.pipeline, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
            w.writeheader()
            w.writerows(linhas)
        print("pipeline gravado em {} ({} registros)\n".format(args.pipeline, len(linhas)))


if __name__ == "__main__":
    main()
