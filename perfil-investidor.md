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

### O que a modalidade determina — observado no estoque de SC

Levantado a cada varredura sobre os lotes coletados. Amostra pequena; serve de
indício, não de regra.

| Modalidade | Lotes | Teto de condomínio atrasado | Permite financiamento |
|---|---|---|---|
| Leilão SFI | 15 | **0** | **0** |
| Licitação Aberta | 1 | 1 | 0 |
| Venda Online | 2 | 2 | 1 |

Duas leituras, com pesos diferentes:

1. **O teto de condomínio acompanha a modalidade.** Nenhum Leilão SFI tem teto;
   todos os lotes fora do SFI têm — "sob responsabilidade do comprador, **até o
   limite de 10% do valor de avaliação**", com a Caixa pagando o excedente.
   Atenção ao que isso é e ao que não é: num lote avaliado em R$ 240 mil, o teto
   é R$ 24 mil. Ele **não melhora o cenário base** (a premissa de triagem é
   R$ 12 mil, abaixo do teto) — ele **elimina a cauda**, o cenário de R$ 20 mil
   ou mais que hoje leva a margem a −18,7%.
2. **O financiamento não acompanha a modalidade.** Dos dois lotes de Venda
   Online, um permite SBPE e o outro é "exclusivamente à vista". A nota de
   estratégia deste perfil diz "Venda Online e Venda Direta com mais
   frequência", e é assim que deve ser lido: **frequência, não garantia**. A
   forma de pagamento se confere lote a lote, na ficha e no edital.

### Como os lotes saem da lista — observado na Grande Florianópolis

Acumulado em `dados/historico-saidas.csv`. **Doze saídas** até 03/10/2026, em
onze Leilões SFI e uma Licitação Aberta. O portal **não declara a causa**:
arremate, suspensão, retirada e purgação da mora são indistinguíveis daqui.

| Constatação | n | Situação |
|---|---|---|
| Nenhum lote saiu entre o 1º e o 2º leilão | 8 de 8 (dos que têm duas datas) | **mantida** |
| Piso na saída, sobre a avaliação | mediana 60,0% (n=12) | mantida |
| Saída exatamente no piso do 2º leilão | 7 de 12 | nova, 03/10 |
| Atraso do portal entre certame e baixa | ~1 dia, 4 vezes | mantida |
| Saiu somente depois de esgotar as duas datas | 10 de 12 | **DERRUBADA — 2 casos contrários** |

Uma retratação a registrar. Em 02/10 anotei como saída o lote de Venda Online do
Estreito (`000001028634-4`); em 03/10 ele **reapareceu na lista**, inalterado. A
ausência de uma rodada era indisponibilidade da fonte, não saída, e o registro
está marcado como `RETRATADO` em `historico-saidas.csv`. A lição é de método:
**uma única ausência não constitui saída** — só se registra o lote ausente em
duas rodadas consecutivas.

A regra deixou de depender da memória de quem executa. Desde 03/10 ela está
**embutida no `historico.py`**, que mantém `dados/ausencias-pendentes.csv`: a
primeira ausência fica em quarentena, a segunda confirma a saída, e o reaparecimento
limpa a quarentena sem ter sujado o histórico. A planilha declara as pendências
na aba Saíram da lista. **Em 04/10 a regra se fechou:** o lote do Centro
reapareceu e saiu da quarentena sem nunca ter entrado no histórico — que segue
com os mesmos doze registros. É o primeiro ciclo completo da regra, do alerta à
absolvição. **Já na primeira aplicação a regra evitou um erro:** na
rodada das 19h de 03/10 faltou o lote de Venda Online do Centro de Florianópolis
(`144440299841-6`, R$ 809.389,16) — exatamente o mesmo padrão, Venda Online e
sem data de certame. Ficou pendente, não registrado.

#### A conclusão que caiu, e a que não caiu

Até 25/09 as cinco saídas observadas tinham esgotado as duas datas de certame, e
daí se concluiu que lote só sai depois do 2º leilão. Ficou registrado que **um
único caso contrário derrubaria a conclusão**. Em 29/09 ele apareceu: o lote
**878770360836-7**, em Bela Vista, deixou a lista **nove dias antes do seu 1º
leilão**, marcado para 08/10. Em 03/10 apareceu o segundo: o lote
**160000012143-0**, no João Paulo, em Florianópolis, saiu **dois dias antes do
seu 1º leilão**, marcado para 05/10. Dois casos não são mais exceção isolada —
é uma via de saída recorrente, e passa a contar como regra de operação.

O que **se mantém**: o 1º leilão não fecha. São agora oito lotes cujo 1º leilão
ocorreu enquanto estavam na lista, e nenhum deles saiu no intervalo entre as duas
datas — o último caso é o lote de São Sebastião (`878771537674-1`), cujo 1º
leilão foi em 02/10 e que segue listado para o 2º, em 08/10. O piso do 2º leilão
continua sendo o preço de entrada correto para a triagem.

E uma constatação nova: **sete das doze saídas ocorreram com o lote marcado
exatamente no piso do 2º leilão**, 60,0% da avaliação. Ou seja, nesta praça o
lote costuma deixar a lista no mínimo legal, não acima dele. Para a formação de
lance isso significa que **pagar prêmio sobre o piso do 2º leilão não é
necessário na mediana dos casos** — ainda que nada garanta o resultado de um
certame individual.

O que **caiu**: a ideia de que a lista só se esvazia por certame. **Existe uma
via de saída antes de qualquer leilão**, e ela tem consequência prática direta —
um lote pode desaparecer durante a due diligence, depois de gasto dinheiro em
matrícula, vistoria e consulta a advogado.

#### Hipótese sobre a causa, declarada como hipótese

Na alienação fiduciária, o devedor pode **purgar a mora** até a assinatura do
auto de arrematação (Lei 9.514/1997, art. 34 e correlatos): quita o débito e
recupera o imóvel, e o lote sai do leilão. É a explicação mais provável para uma
saída anterior ao certame, e não pode ser arremate, porque o certame não
ocorreu. Suspensão judicial e retirada pela Caixa também explicariam.

**Nada disso foi confirmado.** Confirmar exigiria consultar a matrícula
atualizada (a baixa da consolidação da propriedade apareceria averbada) ou o
leiloeiro. Enquanto não se confirmar, o registro guarda o fato — saiu antes do
certame — e nomeia a hipótese como hipótese.

#### O que isso muda no mandato

Quem investe em Leilão SFI **compete com o direito do ex-devedor de recuperar o
imóvel até o último momento**. Isso não é risco de execução, é risco de
existência do ativo, e ele não aparece em nenhuma planilha de viabilidade. Duas
consequências para a operação:

1. **Não adiantar dinheiro de due diligence** em lote cujo certame esteja
   distante. Quanto maior o prazo até o 1º leilão, maior a janela de purgação.
2. **Reconferir a existência do lote no portal na véspera** de qualquer
   desembolso — inclusive o de vistoria e o de honorários.

### O portal responde 200 com a página vazia — e a coleta não pode aceitar

Em 04/10/2026, na rodada das 07h, três lotes tiveram a página de detalhe
respondida **com status 200 e corpo vazio**. O coletor aceitava: não era redireção
e havia corpo. A linha saía inteira em branco, com apenas o número do imóvel, e
dali em diante o erro se propagava em silêncio — a triagem descartava o lote como
`fora_do_bairro`, a planilha o exibia sem preço e, se a falha atingisse a cidade
toda, o diff leria a lista encurtada como **saída de lote que nunca saiu**.

Foi o que quase ocorreu: na mesma rodada, a busca de Florianópolis devolveu
**zero lotes**, o que o antirrobô e uma praça vazia produzem de forma
indistinguível daqui. **A intermitência se confirmou nas 19h do mesmo dia:** a
busca de Florianópolis voltou vazia duas vezes consecutivas e, na terceira,
entregou os dois lotes inalterados. Não é praça vazia — é o portal respondendo
200 sem conteúdo. O coletor passou a repetir também a busca da cidade, até
quatro vezes, e a informar quantas voltas em branco precederam o resultado.

A correção exige, de cada lote, **bairro, preço, avaliação e área privativa**;
repete a página de detalhe até quatro vezes; e **falha em voz alta**, sem gravar
nada, se algum lote não completar ou se a busca de uma cidade vier vazia. É o
mesmo princípio já adotado para os comparáveis de mercado: **dado que falta não
pode parecer dado que é zero.**

### O campo "Desconto" do portal pode ser negativo — e o de 03/10 foi

O lote **000001018127-9**, uma sala comercial no Kobrasol, em São José, saiu da
lista anunciando **R$ 395.960,11 sobre uma avaliação de R$ 250.000,00** —
desconto de **−58,38%**, isto é, um prêmio de 58% sobre o valor avaliado.

Não é erro de coleta: é o mecanismo do SFI. O piso do 2º leilão não é um
percentual da avaliação, e sim **o valor da dívida consolidada somada aos
encargos e às despesas do procedimento** (Lei 9.514/1997, art. 27, §2º, II).
Quando a dívida supera o valor do imóvel — exatamente o caso de uma garantia que
se deteriorou mais rápido que o saldo devedor —, o piso legal sobe acima da
avaliação, e o portal exibe desconto negativo.

Três consequências práticas:

1. O corte de desconto mínimo de 25% da triagem **já descarta esses lotes
   automaticamente**, e é bom que descarte. Nenhum ajuste é necessário.
2. **Desconto alto não significa imóvel barato, e desconto negativo não
   significa erro.** Os dois lados do campo são informação sobre a dívida, não
   sobre o imóvel. O preço de referência é sempre o VVR, nunca a avaliação da
   Caixa — que, como já registrado nesta praça, divergiu 15,7% entre duas
   unidades de mesma metragem e mesmo endereço.
3. Para a perícia, é o indicador de que **a avaliação da Caixa e o saldo devedor
   são grandezas independentes**, e que uma não valida a outra.

## Cortes automáticos

Aplicados pelo `scripts/triagem.py` em toda varredura:

- desconto anunciado mínimo: **25%**
- margem líquida projetada abaixo de 25% sobre o CTA: descarta
- fora da praça-alvo (núcleo + 1º anel): descarta
- acima do ticket máximo: descarta
- sem matrícula individualizada: descarta

## Referência de mercado — Bela Vista, Palhoça

Levantado em **23/09/2026** a partir de anúncios ativos no portal
imoveis-sc.com.br (Bela Vista, Palhoça/SC). Anúncio é preço pedido, não preço
fechado — daí o fator de deságio de 0,88 da tese de saída. Renovado a cada sete
dias pela rotina de varredura.

| Tipologia | Mediana de anúncio | Data | Nº de comparáveis | Fonte |
|---|---|---|---|---|
| Apto 2 dorm. | **R$ 275.000** | 23/09/2026 | 26 | imoveis-sc.com.br |
| Apto 3 dorm. | `INEXISTENTE` — nenhum anúncio no bairro | 23/09/2026 | 0 | imoveis-sc.com.br |
| Casa | **R$ 479.000** | 23/09/2026 | 53 | imoveis-sc.com.br |
| Aluguel apto 2 dorm. | `A LEVANTAR` — fonte não entrega locação | — | 0 | — |

### O número que realmente entra no VVR

A mediana simples se refere a uma área mediana de 49 m². O estoque da Caixa em
Bela Vista é menor (43,80 a 45,61 m²), então usar a mediana crua superestima o
VVR. Normalizado por área:

| Métrica | Valor | Base |
|---|---|---|
| R$/m² mediano — banda 42 a 49 m² | **R$ 5.913** | n=13 — **é esta que se usa** |
| Preço mediano na banda 42–49 m² | R$ 270.000 | n=13 |
| Área mediana anunciada — 2 dorm. | 49 m² | n=26 |
| Condomínio mediano | R$ 399/mês | n=20 |

**Fórmula do VVR em Bela Vista:** `área privativa × R$ 5.913 × 0,88`.

### Série histórica do R$/m² da banda

| Data | R$/m² | n | Variação |
|---|---|---|---|
| 16/09/2026 | R$ 5.920 | 14 | — |
| 23/09/2026 | R$ 5.913 | 13 | −0,1% |

Uma semana de dados não é tendência. A série existe para que, daqui a alguns
meses, se saiba se Bela Vista está valorizando ou não — e para que uma queda
de VVR não seja confundida com mudança no estoque da Caixa.

### Leituras do levantamento

- **Bela Vista é mercado de 2 dormitórios.** Na segunda medição não há **nenhum**
  apartamento de 3 dormitórios anunciado no bairro. A tipologia não tem
  liquidez comprovada ali e não serve à tese de flip.
- A dispersão dos 2 dormitórios permanece entre R$ 230.000 e R$ 350.000.
- **A avaliação da Caixa não é o mercado.** Dois lotes no mesmo endereço (Av.
  Paulo Roberto Vidal, 2050), mesma metragem (50,87 m² totais / 43,80 m²
  privativos) e mesmo CEP foram avaliados em R$ 258.000 e R$ 223.000 —
  **15,7% de diferença entre unidades aparentemente iguais**. E a Caixa rotulou
  um como Bela Vista e o outro como Lot. Pq. Vale Verde.
- **O estoque de Bela Vista caiu de 3 para 2 lotes em 29/09**, com a saída do
  878770360836-7 — que era o único dos três com margem positiva. Ver a seção
  sobre saídas: ele deixou a lista antes do próprio certame.

### A referência de mercado está congelada desde 23/09/2026

Em 30/09 a renovação dos comparáveis **falhou**. As três fontes de anúncios
disponíveis — `imoveis-sc.com.br`, `zapimoveis.com.br` e `vivareal.com.br` —
passaram a responder **HTTP 403 com página de desafio Cloudflare**. Três
tentativas, três bloqueios, em todas elas. A `imoveis-sc.com.br`, que vinha
funcionando desde 16/09, foi a última a cair.

**Consequência:** o R$/m² de R$ 5.913 e a mediana de R$ 275.000 são de
23/09/2026 e **não estão sendo atualizados**. Todo VVR e toda margem calculada
depois dessa data repousam sobre uma referência que envelhece. A cada rodada, a
idade do levantamento deve ser declarada — e desde 03/10 a própria planilha a
declara sozinha, na aba Comparáveis, com advertência de levantamento vencido a
partir do sétimo dia. Em 03/10/2026 o levantamento completou **dez dias**.

**O que isso não é:** não é mercado sem anúncios. A fonte respondeu — apenas
barrou a coleta. O `comparaveis.py` passou a distinguir os dois casos e a falhar
em voz alta, sem gravar arquivo: um CSV de zero linhas gravado em silêncio seria
pior que a falha, porque pareceria um bairro vazio.

**Remédio possível, não implementado:** o ambiente tem Chromium e Playwright
instalados. Um coletor que dirija o navegador de verdade costuma vencer o
desafio do Cloudflare, onde o `curl` não vence. É trabalho de porte e não há
garantia de que funcione — decisão da investidora.

### A revisar

- Locação: nenhuma fonte liberada na política de rede entrega anúncios de
  aluguel do bairro. Sem isso não há cap rate nem plano B de renda enquanto o
  flip não sai.
- Os comparáveis são anúncios, não transações. Preço fechado exigiria ITBI da
  Prefeitura de Palhoça ou consulta a corretor local.
