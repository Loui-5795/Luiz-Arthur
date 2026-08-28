# Análise financeira: CTA, VVR, margem e score

## 1. Custo Total de Aquisição (CTA)

O único número que importa do lado do custo. Nunca compare "lance" com "valor
de mercado" — compare CTA com VVR.

```
CTA = lance
    + comissão do leiloeiro          (~5% do lance, quando há leiloeiro)
    + ITBI                            (2% a 3% conforme o município)
    + registro e escritura            (~1% a 1,5%)
    + débitos assumidos               (IPTU + condomínio + consumo)
    + custo de desocupação            (acordo + honorários + oficial)
    + reforma e regularização         (CAPEX)
    + custo de carrego                (IPTU/condomínio/consumo × meses até a venda)
    + custo do capital                (taxa × valor imobilizado × meses/12)
```

### Faixas de referência para orçar quando não há dado firme

| Rubrica | Faixa típica | Observação |
|---|---|---|
| Comissão do leiloeiro | 5% do lance | Paga à parte; não devolvida em desistência |
| ITBI | 2% – 3% | Base varia por município; confirme |
| Registro + escritura | 1% – 1,5% | Tabela estadual |
| Reforma leve (pintura, elétrica, louças) | R$ 400 – 700 /m² | Imóvel conservado |
| Reforma pesada (estrutura, hidráulica, esquadrias) | R$ 900 – 1.800 /m² | Imóvel depredado — comum em retomados |
| Regularização de área não averbada | R$ 8k – 30k + 6–18 meses | Projeto, ART, taxas |
| Desocupação por acordo | R$ 5k – 25k | Muito mais rápido que processo |
| Desocupação litigiosa | R$ 10k – 40k + 12–36 meses | Honorários + tempo |
| Custo de venda (corretagem) | 5% – 6% do preço | Entra na saída, não no CTA |

> Estas faixas são ponto de partida para triagem, não orçamento. Substitua por
> cotação real assim que o lote sair da triagem.

## 2. Valor de Venda Rápida (VVR)

```
VVR = mediana(anúncios ativos comparáveis) × fator de deságio
```

- Comparáveis: mesmo bairro, mesma tipologia, área dentro de ±15%, mesmo padrão.
  Mínimo de 5. Descarte outliers.
- Fator de deságio por prazo-alvo de venda: **0,92** (180 dias) · **0,88**
  (90 dias) · **0,80** (30–45 dias, venda forçada).
- Anúncio ≠ transação. Se conseguir dados de ITBI ou de um corretor local,
  prefira transação efetiva.
- Para tese de renda, calcule também o **cap rate**:
  `aluguel mensal × 12 / CTA`. Abaixo de 6% ao ano, a tese de renda não fecha.

## 3. Indicadores de decisão

```
Margem líquida    = (VVR × (1 − custo de venda) − CTA) / CTA
Retorno anualizado ≈ (1 + margem líquida) ^ (12 / meses do ciclo) − 1
Desconto real     = 1 − CTA / VVR
```

Critérios de corte sugeridos (ajuste ao mandato do investidor):

| Tese | Margem líquida mínima | Ciclo típico |
|---|---|---|
| Flip / revenda | ≥ 25% | 6 – 12 meses |
| Renda / locação | cap rate ≥ 7% a.a. | perpétuo |
| Uso próprio | desconto real ≥ 20% | — |

**Lance máximo** é o lance que ainda entrega a margem-alvo. É o número que se
leva para o certame, escrito, e do qual não se passa. `viabilidade.py` calcula.

## 4. Pesos do score (0–100)

| Dimensão | Peso | Como pontuar (0–10 antes do peso) |
|---|---|---|
| Margem líquida projetada | 30 | 0 = ≤ 0%; 5 = 25%; 10 = ≥ 50% |
| Liquidez do ativo | 20 | tempo de venda de comparáveis: 10 = < 60 dias; 0 = > 240 dias |
| Segurança jurídica | 20 | 10 = venda direta de banco, matrícula limpa; 5 = licitação/1º leilão; 0 = judicial com embargos ou lance < 50% da avaliação |
| Situação de posse | 15 | 10 = desocupado verificado; 6 = ocupado por ex-devedor; 2 = terceiro; 0 = invasão/usucapião alegada |
| Passivos e reforma | 10 | 10 = sem débitos e reforma leve; 0 = débitos > 15% do CTA ou reforma pesada |
| Prazo e liquidez do caixa | 5 | 10 = prazo folgado ou aceita financiamento; 0 = à vista em 24h sem caixa |

Classificação: **≥ 75 perseguir** · **60–74 acompanhar** · **< 60 descartar**.

Trava: segurança jurídica < 10 pontos ponderados (nota bruta < 5) **nunca** vira
"perseguir" sem parecer de advogado, por mais alta que esteja a margem. Margem
grande em leilão quase sempre é o preço de um risco que alguém já mediu.

## 5. Erros de análise que mais custam dinheiro

1. Usar a avaliação do edital como valor de mercado.
2. Esquecer a comissão do leiloeiro (5% fora do lance).
3. Não orçar o custo de desocupação e do tempo até desocupar.
4. Ignorar o custo de carrego em ciclo de 12+ meses.
5. Orçar reforma por foto.
6. Tratar débito condominial de edital omisso como se fosse zero.
7. Dar lance acima do teto definido, no calor do certame.
