# Perfil do investidor

Parâmetros do mandato. Toda triagem, score e critério de corte deste projeto
lê daqui. Mudou a estratégia? Muda este arquivo, não os scripts.

## Praça-alvo

| | |
|---|---|
| **Núcleo** | Palhoça / SC — bairro **Bela Vista** |
| **1º anel** (incluir na varredura) | Palhoça: Pedra Branca, Passa Vinte, Aririú, Jardim Eldorado, Ponte do Imaruim, Caminho Novo |
| **2º anel** (acompanhar) | São José e Florianópolis continental |
| **Fora** | Restante de SC |

> **Nota de estratégia.** Bela Vista sozinho é um mercado fino para estoque de
> banco — as listas públicas indicam poucos lotes da Caixa no bairro em um dado
> momento. Varrer só ele devolve tela vazia na maioria das semanas. Por isso o
> 1º anel entra na varredura automática: o bairro define onde você *quer*
> comprar, o anel garante que o agente tenha o que analisar e que você conheça
> o comparável quando o lote de Bela Vista aparecer.

## Capital e ticket

| | |
|---|---|
| Capital à vista | **R$ 50.000 a R$ 100.000** |
| Ticket máximo por lote | **decorre do capital, não é fixo** — ver tabela abaixo |
| Aceita financiamento Caixa | `A DEFINIR` — mas é o que muda o jogo, ver nota |
| Aceita usar FGTS | `A DEFINIR` |

### Teto de lance por cenário, com R$ 100 mil de caixa

Calculado por `scripts/viabilidade.py`. O lance não é o custo: comissão de 5%,
ITBI, registro, dívidas, desocupação, reforma e carrego saem do mesmo bolso.

| Cenário | Custos fixos | **Teto de lance** | Limitado por |
|---|---|---|---|
| Apto 45 m², desocupado, sem dívidas | R$ 24,7 mil | **R$ 69,0 mil** | caixa |
| Apto 60 m², ocupado pelo ex-devedor, condomínio atrasado | R$ 75,5 mil | **R$ 22,4 mil** | caixa |
| Apto 60 m², ocupado por terceiro, dívida alta | R$ 113,3 mil | **inviável** | o capital não cobre nem os custos |
| Apto 60 m² desocupado, **financiado com 20% de entrada** | R$ 37,8 mil | **R$ 144,2 mil** | margem |

Com R$ 50 mil, todos os tetos à vista caem para menos da metade — na prática,
sobra terreno e lote de valor muito baixo.

> **Nota sobre financiamento.** É a única alavanca que coloca um apartamento de
> Bela Vista ao alcance deste capital. Mas vale só onde o edital do lote admite:
> Venda Online e Venda Direta com mais frequência; modalidades com leiloeiro
> costumam exigir pagamento à vista em prazo curto. Exige **crédito
> pré-aprovado antes do certame**.
>
> Limite do modelo atual: as parcelas do financiamento durante o ciclo ainda não
> entram no cálculo do carrego. Antes de dar lance financiado, somar
> `parcela × meses` ao desembolso.

## Tese de saída

| | |
|---|---|
| Tese principal | **Revenda (flip)** |
| Ciclo aceitável | 6 – 12 meses da arrematação à venda |
| Margem líquida mínima | **25% sobre o CTA** — abaixo disso, descarta |
| Custo de venda a considerar | 6% de corretagem |
| Fator de deságio do VVR | 0,88 (venda em 90 dias) |

## Tolerâncias

| | |
|---|---|
| Ocupação | `A DEFINIR` — mas na tese de flip, imóvel ocupado come o ciclo inteiro: prazo de desocupação acima de 6 meses inviabiliza a margem |
| Risco jurídico | `A DEFINIR` — em flip, anulação de arrematação trava o capital por anos; começar por Venda Direta, Venda Online e Licitação Aberta |
| Tipologia | apartamento e casa residencial; terreno só com acesso e matrícula limpa |

### O que consome o capital, por bloco

Ordem de grandeza para triagem; substituir por cotação real na due diligence.

| Bloco | Faixa | Como descobrir o valor real |
|---|---|---|
| Comissão do leiloeiro | 5% do lance, à parte | Edital do lote |
| ITBI | 2% a 3% | Prefeitura de Palhoça |
| Registro e escritura | 1% a 1,5% | Tabela de emolumentos de SC |
| Condomínio atrasado | R$ 0 a R$ 20 mil | Administradora, **por escrito e com data** |
| IPTU atrasado | R$ 1 a 5 mil | Prefeitura. Em hasta pública, sub-roga no preço (Tema 1.134 STJ) |
| Desocupação por acordo | R$ 5 a 25 mil | Depende de quem ocupa |
| Desocupação litigiosa | R$ 10 a 40 mil + 12 a 36 meses | Advogado |
| Reforma leve | R$ 400 a 700 /m² | Orçamento após vistoria |
| Reforma pesada | R$ 900 a 1.800 /m² | Orçamento após vistoria |
| Regularização de área não averbada | R$ 8 a 30 mil + 6 a 18 meses | Projeto, ART, taxas |
| Carrego | mensal × meses | Condomínio + IPTU + consumo |

## Cortes automáticos

Aplicados pelo `scripts/triagem.py` em toda varredura:

- desconto anunciado mínimo: **25%**
- margem líquida projetada abaixo de 25% sobre o CTA: descarta
- fora da praça-alvo (núcleo + 1º anel): descarta
- acima do ticket máximo: descarta
- sem matrícula individualizada: descarta

## Referência de mercado — Bela Vista, Palhoça

Levantado em **16/09/2026** a partir de anúncios ativos no portal
imoveis-sc.com.br (Bela Vista, Palhoça/SC). Anúncio é preço pedido, não preço
fechado — daí o fator de deságio de 0,88 da tese de saída.

| Tipologia | Mediana de anúncio | Data | Nº de comparáveis | Fonte |
|---|---|---|---|---|
| Apto 2 dorm. | **R$ 278.000** | 16/09/2026 | 23 | imoveis-sc.com.br |
| Apto 3 dorm. | `INSUFICIENTE` — n=1, R$ 515.000 | 16/09/2026 | 1 | imoveis-sc.com.br |
| Casa | **R$ 480.000** | 16/09/2026 | 54 | imoveis-sc.com.br |
| Aluguel apto 2 dorm. | `A LEVANTAR` — fonte não entrega locação | — | 0 | — |

### O número que realmente entra no VVR

A mediana simples de R$ 278.000 se refere a uma área mediana de **46,9 m²**. O
estoque da Caixa em Bela Vista é menor (43,80 a 45,61 m²), então usar a mediana
crua superestima o VVR. Normalizado por área:

| Métrica | Valor | Base |
|---|---|---|
| R$/m² mediano — apto 2 dorm. | **R$ 5.859** | n=22 com área declarada |
| R$/m² mediano — banda 42 a 49 m² | **R$ 5.920** | n=14 — **é esta que se usa** |
| Faixa de R$/m² observada | R$ 4.426 a R$ 7.348 | n=22 |
| Preço mediano na banda 42–49 m² | R$ 262.000 | n=14 |
| Área mediana anunciada | 46,9 m² | n=22 |
| Condomínio mediano | R$ 400/mês (R$ 311 a R$ 700) | n=16 |

**Fórmula do VVR em Bela Vista:** `área privativa × R$ 5.920 × 0,88`.

### Leituras do levantamento

- **Bela Vista é mercado de 2 dormitórios.** Dos 24 apartamentos anunciados, 23
  são de 2 dormitórios. Não há amostra para precificar 3 dormitórios, e a
  tipologia provavelmente não existe em volume no bairro — o que também
  significa que ela não tem liquidez comprovada para a tese de flip.
- A faixa de R$ 175 mil a R$ 750 mil do levantamento inicial era de Palhoça
  inteira. Fechada em Bela Vista e por tipologia, a dispersão cai para
  R$ 230.000 – R$ 350.000 nos 2 dormitórios.
- **A avaliação da Caixa não é o mercado, nos dois sentidos.** Dois lotes no
  mesmo endereço (Av. Paulo Roberto Vidal, 2050), mesma metragem (50,87 m²
  totais / 43,80 m² privativos) e mesmo CEP foram avaliados em R$ 258.000 e
  R$ 223.000 — **15,7% de diferença entre unidades aparentemente iguais**. E a
  Caixa rotulou um como Bela Vista e o outro como Lot. Pq. Vale Verde.

### A revisar na próxima varredura

- Locação: nenhuma fonte liberada na política de rede entrega anúncios de
  aluguel do bairro. Sem isso não há cap rate nem plano B de renda enquanto o
  flip não sai.
- Os comparáveis são anúncios, não transações. Preço fechado exigiria ITBI da
  Prefeitura de Palhoça ou consulta a corretor local.
