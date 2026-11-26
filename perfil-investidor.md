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

Acumulado sobre **33 lotes distintos** já observados, de 16/09 a 08/10/2026.
Recalculado pelo `scripts/panorama.py` em cada varredura — nunca à mão.

| Modalidade | Lotes | Teto de condomínio atrasado | Permite financiamento | Aceita FGTS |
|---|---|---|---|---|
| Leilão SFI | 28 | **0** | **1** | 22 |
| Licitação Aberta | 2 | 2 | **1** | 2 |
| Venda Online | 3 | 3 | 2 | 1 |

Duas leituras, com pesos diferentes:

1. **O teto de condomínio acompanha a modalidade.** Nenhum Leilão SFI tem teto;
   todos os lotes fora do SFI têm — "sob responsabilidade do comprador, **até o
   limite de 10% do valor de avaliação**", com a Caixa pagando o excedente.
   Atenção ao que isso é e ao que não é: num lote avaliado em R$ 240 mil, o teto
   é R$ 24 mil. Ele **não melhora o cenário base** (a premissa de triagem é
   R$ 12 mil, abaixo do teto) — ele **elimina a cauda**, o cenário de R$ 20 mil
   ou mais que hoje leva a margem a −18,7%.
2. **O financiamento não acompanha a modalidade — e em 07/10 isto ficou
   demonstrado nos dois sentidos.** Dos três lotes de Venda Online, dois
   permitem financiamento e um é "exclusivamente à vista". E, sobretudo,
   **apareceu o primeiro Leilão SFI que aceita financiamento**: o lote
   `810110001631-4`, apartamento no Córrego Grande, em Florianópolis,
   R$ 480.000 — um em vinte e oito. A nota de estratégia deste perfil diz
   "Venda Online e Venda Direta com mais frequência", e é assim que deve ser
   lida: **frequência, não garantia, nem exclusividade**. A forma de pagamento
   se confere lote a lote, na ficha e no edital — e nunca se presume pela
   modalidade, em nenhuma das duas direções.

   **Correção de registro.** Até 06/10 esta tabela anotava zero financiamentos
   em Leilão SFI, e eu afirmei à investidora que nenhum lote de Palhoça aceitava
   financiamento. A segunda afirmação segue verdadeira — nenhum dos sete lotes
   de Palhoça aceita. A primeira **era verdadeira para a amostra de então e
   deixou de ser**: o estoque mudou, e é por isso que esta tabela se recalcula a
   cada varredura em lugar de ser consultada de memória.

3. **O par FGTS + financiamento no mesmo lote apareceu uma única vez.** O lote
   `160000016077-0`, apartamento em Areias, São José, 186,64 m² a R$ 555.738,07,
   Venda Online, aceita **os dois**. É o primeiro de 32 nessa condição. Está
   fora do bairro-alvo e muito acima do ticket, e por isso a triagem o descarta;
   registra-se porque demonstra que a combinação existe nesta praça — e é
   justamente ela que romperia a restrição de capital que hoje reprova todos os
   lotes de Bela Vista.

### Como os lotes saem da lista — observado na Grande Florianópolis

Acumulado em `dados/historico-saidas.csv`. **Vinte e uma saídas** até
13/11/2026, em dezessete Leilões SFI e **quatro** Licitações Abertas — **nenhuma em
Venda Online**, e isso não é lacuna, é consequência de regra, pelo motivo exposto
adiante.

A segunda Licitação Aberta, confirmada em 30/10, é a primeira observação útil
sobre a modalidade de **data única**: o apartamento `144442282177-5`, no
Estreito, Florianópolis, R$ 499.017,10, teve certame em 29/10 e ausentou-se na
manhã de 30/10, confirmando-se à noite. **O atraso de cerca de um dia entre o
certame e a baixa no portal, até aqui medido só em Leilão SFI, repete-se na
Licitação Aberta** — o que era de esperar, por ser atraso de processamento do
portal e não característica do certame, mas que só agora se observou.

**Três delas foram verificadas prospectivamente**, e são as de maior valor
probatório de toda a série, porque a data foi anunciada antes e conferida
depois:

| Lote | Bairro | Preço | 1º leilão | 2º leilão | Ausente em |
|---|---|---|---|---|---|
| `878771537674-1` | São Sebastião | R$ 186.000 | 02/10 | 08/10 | 09/10, manhã |
| `144441088173-5` | Pagani | R$ 330.300 | 05/10 | 09/10 | 10/10, manhã |
| `878770561220-5` | **Bela Vista** | R$ 151.200 | 05/10 | 09/10 | 10/10, manhã |
| `878771588251-5` | **Bela Vista** | R$ 168.933 | 14/10 | 20/10 | 21/10, manhã |
| `878771222509-2` | Areias, São José | R$ 154.257 | 14/10 | 20/10 | 21/10, manhã |
| `144441762824-5` | Forquilhinha, São José | R$ 185.855 | 20/10 | 26/10 | 27/10, manhã |
| `844441802944-0` | Barreiros, São José | R$ 315.337 | — | 04/11 (data única) | 05/11, manhã |

As duas de 21/10 foram anunciadas em 15/10 e repetidas em cinco rodadas, com a
data da saída prevista antes de ocorrer. **Sete previsões, sete confirmações.**
A oitava foi feita em 24/11/2026 e está em aberto: ou o lote de Aririú da
Formiga permanece fora da lista, ou reaparece em Venda Online até cerca de
29/11. Ver a seção daquela data.

A sétima é a de maior valor probatório da série, por três razões. Foi a única
**anunciada dois dias antes** do fato, em 03/11, e repetida em três rodadas. Foi
a primeira feita em **Licitação Aberta**, modalidade de data única, cujo prazo de
baixa se havia medido uma única vez, em 30/10 — de sorte que a previsão extrapolou
de n=1 e se confirmou. E o lote **permaneceu listado na rodada da noite do próprio
certame**, confirmando que a baixa no portal se dá na manhã seguinte, e não no
dia.

A sexta merece registro próprio, por nascer de um erro meu. Em 21/10 anunciei
"três 2º leilões em 20/10" e incluí Forquilhinha entre eles; os certames do lote
são **20/10 e 26/10**, de modo que 20/10 era o seu **1º** leilão. Corrigida a
classificação, a previsão passou a ser a saída na manhã de 27/10 — e foi o que
se observou, com a primeira ausência às 07h e a confirmação às 19h do mesmo dia.
**A previsão original não falhou por acaso: ela não existia, porque o estágio
estava mal classificado.** O acerto desta sexta linha é o da regra, não o da
pressa.

Os três permaneceram listados entre as duas datas e saíram na manhã seguinte ao
2º leilão. O terceiro era **um dos lotes aprovados na triagem** — o melhor
colocado da praça-alvo. Sua saída não representa perda de oportunidade: ele
reprovava no mandato por margem de −5,5% e estava fora do alcance do caixa.
Representa, isso sim, que **a janela existe e se fecha**, e que o acompanhamento
mede essa janela com precisão de um dia. O portal **não declara a causa**:
arremate, suspensão, retirada e purgação da mora são indistinguíveis daqui.

| Constatação | n | Situação |
|---|---|---|
| Nenhum lote saiu entre o 1º e o 2º leilão | **13 de 13** (dos que têm duas datas) | **mantida — 6 previstas** |
| Piso na saída, sobre a avaliação | mediana 60,0% (n=16) | mantida |
| Saída exatamente no piso do 2º leilão | 10 de 16 | mantida |
| Atraso do portal entre certame e baixa | **~1 dia, 7 vezes** — 3 delas previstas | **reforçada em 10/10** |
| Saída posterior ao certame | **19 de 21** | **medida em 24/11** |
| Licitação Aberta: saída em `+1` dia do certame único | **5 de 5** | **medida em 24/11** |
| Saída em `+1` dia significa arremate | 3 de 4 não voltaram | **não se afirma — n pequeno** |
| Saiu somente depois de esgotar as duas datas | 14 de 16 | **DERRUBADA — 2 casos contrários** |

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

O que **se mantém**: o 1º leilão não fecha. São agora **dez** lotes cujo 1º
leilão ocorreu enquanto estavam na lista, e nenhum deles saiu no intervalo entre
as duas datas. Os dois últimos casos foram observados em 06/10, e são os mais
limpos da série porque o 1º leilão foi acompanhado em tempo real: o lote de
**Bela Vista** (`878770561220-5`, R$ 151.200) e o do **Pagani**
(`144441088173-5`, R$ 330.300) tiveram 1º leilão em 05/10 e seguiam listados,
com preço, desconto e datas inalterados, na manhã seguinte. O 2º leilão de ambos
é em 09/10. Antes deles, o lote de São Sebastião (`878771537674-1`), 1º leilão em
02/10, segue listado para o 2º em 08/10.

A constatação já se sustenta em dez observações e **ainda assim não é lei**: ela
descreve o comportamento desta praça neste período, e um único caso contrário a
derruba — como ocorreu, em 29/09, com a conclusão vizinha sobre esgotamento das
datas. O que ela autoriza é operacional e limitado: **não há razão para formar
lance para o 1º leilão nesta praça**, porque o preço de entrada relevante é o
piso do 2º. O piso do 2º leilão
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

#### Erro meu de classificação, corrigido em 21/10/2026

Em 15/10 anunciei "três 2º leilões em 20/10" e repeti o anúncio em cinco
rodadas, até 19/10, com previsão de que os três sairiam da lista em 21/10.
**Dois saíram; o terceiro não — e o terceiro não deveria sair.**

| Lote | Certames | O que 20/10 era | Resultado em 21/10 |
|---|---|---|---|
| Bela Vista, P. R. Vidal, 2050 | 14/10 e 20/10 | **2º leilão** | ausente ✔ |
| Areias, São José | 14/10 e 20/10 | **2º leilão** | ausente ✔ |
| Forquilhinha, São José | **20/10** e 26/10 | **1º leilão** | segue listado ✔ |

O lote de Forquilhinha tem certames em **20/10 e 26/10**: a data de 20/10 era o
seu **primeiro** leilão, não o segundo. Eu o agrupei com os outros dois por
coincidência de data, sem conferir a que etapa a data correspondia em cada um.

**A previsão não falhou — a minha classificação falhou.** E o resultado, bem
lido, confirma as duas constatações ao mesmo tempo: os dois lotes de 2º leilão
saíram na manhã seguinte, e o de 1º leilão permaneceu, elevando a constatação do
1º leilão a **doze de doze**. O 2º leilão de Forquilhinha é em 26/10, e a
previsão correta para ele é a saída na manhã de 27/10.

**A lição, que é de disciplina e não de método:** agrupar por data é cômodo e
engana. A data de um certame só significa algo acompanhada da etapa a que
corresponde — primeiro ou segundo leilão —, e etapa se lê no campo, lote a lote,
nunca por semelhança com o vizinho. Em perícia, é o mesmo vício de somar
documentos pela data de emissão sem verificar a que competência cada um se
refere.

#### Na Venda Online, ausência da lista não é saída — 16/10/2026

A regra das duas rodadas reduziu os falsos positivos, mas não os eliminou, e o
caso que a expôs é definitivo. O lote **144440299841-6**, apartamento no Centro
de Florianópolis, Venda Online, R$ 809.389,16:

- ausentou-se da lista em 10/10, às 07h;
- a saída foi **confirmada** pela regra das duas rodadas em 10/10, às 19h;
- permaneceu ausente por **treze rodadas consecutivas**;
- **reapareceu intacto** em 16/10, às 07h.

Nenhuma janela finita de confirmação o teria poupado. Duas rodadas não bastam,
nem dez bastariam.

**O placar por modalidade é inequívoco:** dos dois registros de Venda Online que
chegaram ao histórico, **os dois eram falsos** — o do Estreito, retratado em
03/10, e este. Dos quatorze de Leilão SFI, **nenhum**.

A explicação é estrutural e estava à vista desde 02/10: **o lote com certame sai
da lista por um evento datado; o de oferta contínua some e volta ao sabor do
processamento de propostas.** Não há, na Venda Online, evento algum cuja
ocorrência a ausência possa indicar.

**Regra adotada:** lote **sem data de certame não entra no histórico de
saídas**. Vai para `dados/ausencias-venda-online.csv`, registro próprio que
descreve o que se observou — *ausente da lista* — e não afirma o que não se
sabe. Ambos os registros falsos foram retratados; o histórico passa a quinze
saídas, todas de modalidades com certame.

**A lição de método, que é a mais dura desta série:** a regra das duas rodadas,
criada em 03/10 justamente para evitar este erro, **não era errada — era
insuficiente, e pelo motivo de sempre: aplicava a mesma prova a fatos de
natureza diferente.** Exigir confirmação em duas rodadas supõe que a ausência
signifique algo; onde não significa, nenhuma quantidade de confirmação produz
significado. Em perícia, o equivalente é exigir o mesmo documento para fatos que
se provam por meios distintos — rigor aparente que não decide nada.

**Terceira confirmação da regra, em 22/10/2026.** O lote **160000016077-0**,
apartamento em Areias, São José, Venda Online, R$ 555.738,07, ausentou-se da
lista em 16/10 às 19h, reapareceu, e ausentou-se outra vez em 22/10 às 19h. Pela
regra anterior, a segunda ausência teria produzido o terceiro registro falso do
histórico; pela regra vigente, produziu uma linha em
`dados/ausencias-venda-online.csv` e nada mais. **O mesmo lote ausentando-se
duas vezes em seis dias é a demonstração direta do que se afirmou acima:** na
oferta contínua, a ausência é intermitência de processamento, não evento.

**Quarta confirmação, em 29/10/2026.** O lote `000001028634-4`, imóvel
comercial de 577,10 m² no Estreito, Florianópolis, Venda Online, R$
1.934.248,90, ausentou-se outra vez. É precisamente o lote da **primeira
retratação**, de 02/10, e sua nova ausência vai para o registro de ausências
sem tocar o histórico. Quatro casos, três lotes distintos, nenhum registro
falso desde a adoção da regra.

**Quinta confirmação, em 30/10/2026.** O mesmo lote do Estreito reapareceu
intacto na rodada seguinte à ausência de 29/10 — uma única rodada fora da
lista. É a segunda reaparição deste lote e a quinta observação sob a regra:
**cinco ausências de Venda Online, três lotes, nenhum registro falso.**

**Verificação prospectiva da regra, em 23/10/2026.** Na rodada das 19h de 22/10
declarou-se que aquela ausência não constituía saída. Na rodada seguinte, às 07h
de 23/10, **o lote reapareceu intacto** — mesmo preço, mesma avaliação, mesma
modalidade —, depois de uma única rodada de ausência. Registre-se o que esta
confirmação é e o que não é: trata-se de **previsão negativa** — afirmou-se que
nada havia ocorrido —, e por isso ela não integra a tabela de previsões de
saída, que só admite data anunciada antes do fato. Classificá-la ali inflaria a
série com um acerto de outra natureza, que é precisamente o erro cometido em
21/10 ao agrupar certames por data.

#### A regra do R$/m² validada em cinco lotes — 13/10/2026

O edital **0053/0226 - CPA/RE** trouxe seis lotes novos em Palhoça, três deles em
Bela Vista, e com isso a amostra chegou a cinco aprovados de metragens e preços
distintos. O resultado é a validação limpa da regra de seleção enunciada em
06/10, e vale registrá-lo com os números:

| Lote | R$/m² de entrada | Equilíbrio no m² | Desconto anunciado | Margem |
|---|---|---|---|---|
| Barra do Aririú (`844442659658-8`) | **R$ 2.983** | R$ 3.233 | 40,00% | **+5,9%** |
| Bela Vista — P. R. Vidal, 475 | R$ 3.155 | R$ 3.267 | 40,00% | +2,6% |
| Bela Vista — S. Alzemiro, 387 | R$ 3.452 | R$ 3.191 | 40,00% | −5,5% |
| Bela Vista — P. R. Vidal, 2050 | R$ 3.857 | R$ 3.191 | 34,52% | −12,9% |
| Bela Vista — edital 0053 | R$ 4.041 | R$ 3.191 | 29,20% | −15,9% |

**A ordenação por preço por metro quadrado reproduz exatamente a ordenação das
margens — cinco de cinco, sem inversão.** A ordenação por desconto anunciado não
reproduz: os três primeiros lotes têm o **mesmo** desconto de 40,00% e margens
que vão de +5,9% a −5,5%, isto é, uma amplitude de 11,4 pontos dentro de um
desconto idêntico.

Fica assim demonstrado, e não apenas conjecturado, que **o desconto da Caixa não
ordena oportunidades e o preço por metro quadrado ordena.** A triagem segue
usando o desconto como corte de entrada, o que é adequado — ele filtra o lote
cuja dívida consolidada encareceu o piso —, mas **a priorização entre os
aprovados deve ser pelo R$/m²**.

**Novo melhor da série:** o lote de **Barra do Aririú**, R$ 138.000 em 46,26 m²,
com margem de **+5,9%** — o primeiro acima de 5% desde 16/09. Reprova no mandato,
por estar muito abaixo dos 25%, e segue fora do alcance do caixa. Certames em
01/12 e 07/12.

#### A Caixa deixou de publicar a ocupação — 10/10/2026

Na rodada das 07h, **os dezessete lotes perderam o campo `Situação` ao mesmo
tempo**. Não é fato do mercado: nenhum evento desocupa dezessete imóveis entre
as 19h e as 07h. Verifiquei três páginas de detalhe e a palavra "Situa" não
aparece mais no HTML; no lugar surgiram dois campos novos, **"Averbação dos
leilões negativos"** e **"Inscrição imobiliária"**. A Caixa reformulou a página
e **deixou de declarar a situação de ocupação**.

O que se fez, em três frentes:

1. **Não se supõe ocupação nenhuma.** O coletor grava `NAO DECLARADO`, nunca
   vazio — campo vazio se confunde com desocupado, e supor desocupação é supor
   em favor da operação. Os dois campos novos passaram a ser coletados; a
   averbação dos leilões negativos interessa diretamente à due diligence.

2. **Corrigiu-se um viés que o silêncio criou.** A triagem dava nota 5 a
   ocupação desconhecida e 4 a ocupação declarada, de modo que a omissão da
   fonte **melhorou o escore de todos os lotes** — um deles subiu de 47,9 para
   50,4 sem que nada no imóvel tivesse mudado. A ausência de informação não pode
   valer mais que a informação ruim. A nota passou a ser a de ocupado, com o
   rótulo `OCUP. PRESUMIDA`, e a justificativa é a base observada, não
   pessimismo: **dos 33 lotes distintos coletados nesta praça enquanto o campo
   existia, 33 estavam ocupados — nenhuma exceção.** Quem desfaz a presunção é a
   vistoria, nunca o silêncio do portal.

3. **Criou-se o controle que detecta esta classe de perda**, em
   `scripts/conferir_coleta.py`: compara o preenchimento de cada campo entre
   duas coletas e **para a rodada** quando um campo que vinha em 80% ou mais dos
   lotes cai abaixo de 20%. Também avisa quando um campo passa a vir preenchido,
   que é sinal de dado novo a aproveitar. Verificado contra a coleta defeituosa
   desta manhã: acusou `Situacao` de 100% para 0% e saiu com erro.

**A regra que isto firma:** campo que esvazia para todos os lotes de uma vez é
mudança na fonte, não fato do mercado. Vale para qualquer base de dados de
terceiro — e para a perícia, é o teste que distingue alteração de realidade de
alteração de critério de registro.

#### A data não identifica a rodada — defeito encontrado em 09/10/2026

A regra das duas rodadas, criada em 03/10 e embutida no `historico.py`, tinha
dois defeitos que só a primeira confirmação real revelou. Ficam registrados
porque ambos produziam erro silencioso.

**Primeiro: a quarentena nunca se esvaziava.** O script procurava os ausentes na
*diferença* entre a coleta anterior e a atual. Um lote já em quarentena estava
ausente de ambas, logo nunca reaparecia nesse conjunto — e ficava preso
indefinidamente. A regra prometia confirmar a saída em duas rodadas e **não
confirmava nenhuma**. O critério correto é a ausência na coleta **atual**, não a
diferença entre duas.

**Segundo, e mais sutil: a data não identifica uma rodada.** São duas por dia,
às 07h e às 19h, e a quarentena guardava apenas `09/10/2026`. Ao comparar essa
marca com a data corrente, o script não distinguia manhã de noite: um lote
ausente pela primeira vez às 19h era tratado como ausente desde rodada anterior
e **confirmado como saída na mesma rodada em que faltou** — precisamente o erro
que a regra existia para impedir. Foi o que aconteceu com o lote de Areias, cuja
confirmação indevida foi desfeita pelo histórico do repositório.

A correção identifica a rodada **pelo nome do arquivo de coleta**
(`2026-10-09-19h`), não pela data, e o script passou a ser idempotente:
reexecutar a mesma rodada não duplica nem antecipa nada. Quatro cenários
verificados em dados sintéticos antes de voltar ao dado real — primeira falta,
reexecução da mesma rodada, confirmação na rodada seguinte e reaparecimento.

**A lição, que vale além deste script:** uma regra de controle precisa de
**identificador de evento**, não de data. Em escrituração, é a diferença entre
numerar o lançamento e datá-lo — dois lançamentos do mesmo dia são
indistinguíveis pela data, e qualquer conferência que se apoie nela confundirá
um com o outro.

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
encargos e às despesas do procedimento** (Lei 9.514/1997, art. 27, §2º, II, na
redação original — **a Lei 14.711/2023 alterou esse parágrafo e o texto vigente
não pôde ser conferido; ver a ressalva na seção de 25/11/2026**).
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

### Sair da lista não é estado permanente — 11/11/2026

O lote **878771588251-5**, apartamento de 43,80 m² na Avenida Paulo Roberto
Vidal, 2050, em Bela Vista, **voltou à lista**. É o mesmo lote cuja saída se
confirmou em 21/10 e que figura entre as previsões prospectivas desta série.

| | Saída, 21/10 | Retorno, 11/11 |
|---|---|---|
| Edital | 0048/0226 - CPA/RE | **0061/0226 - CPA/RE** |
| Certames | 14/10 e 20/10/2026 | **19/01 e 25/01/2027** |
| Avaliação | R$ 258.000,00 | R$ 258.000,00 |
| Preço | R$ 168.932,94 | **R$ 169.635,01** |

**O registro de 21/10 não se retrata, e nada nele estava errado.** O lote
esteve de fato ausente por vinte e uma rodadas, e o histórico sempre registrou
o fato observado — *saiu da lista* — sem supor a causa. O que esta rodada
acrescenta é a causa, por eliminação: **o lote não foi arrematado.** Os dois
leilões de outubro foram negativos, a Caixa recolheu o imóvel e o reofertou
três semanas depois, em edital novo, com datas novas.

**Três consequências práticas, e a terceira é a que interessa ao lance:**

1. **Saída não é venda.** Das vinte saídas registradas, ao menos esta não o
   foi. Quantas mais, não se sabe — e é por isso que a observação nunca foi
   anotada como arremate.
2. **A janela que se fecha pode reabrir.** Perder um lote no certame não o
   perde definitivamente; convém reencontrá-lo, e o acompanhamento o faz
   sozinho.
3. **O preço de reoferta quase não cedeu: +0,42% em vinte e dois dias.** Não é
   reajuste de mercado, é acréscimo de dívida — coerente com o art. 27, §2º,
   II, da Lei 9.514/1997, em que o piso do 2º leilão é a dívida consolidada.
   **Esperar o lote rodar outra vez não o barateia; encarece-o devagar.** Quem
   contava com desconto adicional a cada praça frustrada contava com o que esta
   praça não dá.

**Defeito próprio, corrigido na mesma rodada.** O `historico.py` deduplicava as
saídas **pelo lote**, de modo que uma segunda saída do mesmo imóvel seria
descartada em silêncio — justamente o dado que mede quantas vezes um lote roda
sem ser arrematado. A chave passou a ser **(data, lote)**, e o caso foi testado
nos dois sentidos: duas saídas do mesmo lote em datas distintas entram ambas;
a repetição exata continua sendo descartada.

### A lei de preços do Leilão SFI, medida por inteiro — 25/11/2026, 19h

Coleta íntegra: 20 lotes em Palhoça, 31 no 2º anel, 51 no total. Nenhuma saída,
nenhuma alteração de preço, e **dois lotes novos** — `844441253376-7`
(apartamento de 59,29 m²) e `844441910448-9` (casa de 60,91 m²), ambos em
Potecas, São José, ambos do edital inédito **0063/0226 - CPA/RE**, ambos a
0,600000 da avaliação, com certames em **25/01 e 29/01/2027**. Fora da
praça-alvo; a triagem os descarta por bairro, corretamente.

A rodada serviu para outra coisa. Ao conferir qual preço o coletor registra em
lote com dois leilões, deparei-me com a estrutura completa de preços do Leilão
SFI, que até aqui eu conhecia pela metade.

#### O que o campo `Preco` contém, e por que isso importa

O coletor grava `preço único **ou** 2º leilão **ou** 1º leilão`, nessa ordem —
isto é, **o piso efetivo de entrada**. Em lote de Leilão SFI, portanto, o
`Preco` do dossiê é o mínimo do **2º** leilão, e é essa a base de todos os
descontos já reportados. Confirmado: está correto, e é o número que interessa a
quem quer arrematar. Mas as colunas `Preco 1o leilao` e `Preco 2o leilao`
estavam ali, coletadas e nunca medidas.

#### Medidas as duas, a regra aparece inteira — 57 lotes

| Fator do **1º leilão** (preço ÷ avaliação) | Lotes |
|---|---|
| **1,000000 exato** | **51** |
| de 1,000037 a 1,084908 | 6 |

| Fator do **2º leilão** | Lotes |
|---|---|
| **0,600000 exato** | 33 |
| acima de 0,600000 (até 1,583840) | 24 |
| **abaixo de 0,600000** | **zero** |

**O 1º leilão pede a avaliação — exatamente ela, em cinquenta e um de cinquenta
e sete lotes.** Nos seis restantes pede um pouco mais, e esses seis são
precisamente os lotes cuja dívida consolidada excede a avaliação. **O 2º leilão
nunca desce de 60% da avaliação, em nenhum dos cinquenta e sete.**

A regra, então, é esta — e explica todo o estoque observado:

> **1º leilão = o maior entre a avaliação e a dívida consolidada.**
> **2º leilão = o maior entre 60% da avaliação e a dívida consolidada.**

É o que produz, de uma vez, os trinta e três lotes parados no 0,600000 (dívida
abaixo de 60% da avaliação) e os vinte e quatro acima dele, inclusive o caso do
desconto negativo a 1,583840 (dívida muito acima). **Não há dois regimes: há uma
fórmula com um piso.**

#### Uma correção ao que escrevi, e uma dúvida que não posso resolver daqui

Registrei em 03/10 que os 0,600000 são "o piso legal do 2º leilão". **A
expressão é imprecisa e precisa ser retificada em dois pontos.**

O primeiro: pelo art. 27 da Lei 9.514/1997 na redação original, o piso do 2º
leilão é **o valor da dívida e encargos** — não um percentual da avaliação. Nos
trinta e três lotes em que a dívida é menor, os 60% são, portanto, **piso
comercial da Caixa, acima do mínimo legal**, e não exigência da lei. A distinção
tem consequência prática: **piso de lei não se discute; piso de política, em
tese, muda** — por decisão do vendedor, não por insistência do arrematante.

O segundo, e é aqui que paro: **a Lei 14.711/2023 alterou o § 2º do art. 27**, e
pesquisa em fontes secundárias indica que passou a haver referência a percentual
da avaliação, além de haver decisão do STJ (REsp 2.096.465/SP, rel. min. Ricardo
Villas Bôas Cueva) no sentido de que, após essa lei, não se aceita no 2º leilão
lance inferior à **metade do valor de avaliação**, ainda que superior à dívida.

**Não afirmo o conteúdo do dispositivo vigente, porque não consegui lê-lo.** O
`planalto.gov.br` não está entre os domínios permitidos do ambiente, e a
tentativa de acesso falhou na resolução do nome. **Citar artigo de lei a partir
de resumo de terceiro, num dossiê que a senhora pode levar a juízo, seria
exatamente o vício que este arquivo existe para evitar** — e pior do que não
citar.

Fica, pois, assim consignado: **a estrutura de preços está medida e é fato
observado; a sua fundamentação legal está parcialmente em aberto**, por falta de
acesso ao texto oficial. Pedi a liberação do domínio e aguardo a decisão. Nada
do que foi calculado nesta série depende dessa resposta: os descontos, os CTA e
as margens saem dos preços publicados, não da interpretação do artigo.

### Os três voltaram, e a ausência da Venda Online tem hora do dia — 25/11/2026

Coleta íntegra: 20 lotes em Palhoça, 29 no 2º anel, 49 no total. **A previsão de
ontem resolveu-se na primeira rodada seguinte, e do modo mais limpo possível.**

**Os três lotes de Venda Online que haviam desaparecido voltaram — todos,
pelos preços idênticos, sem exceção.** Voltou ainda um quarto, o apartamento
`144440299841-6` do Centro de Florianópolis, que também já tinha histórico de
ausências. **Era oscilação do portal, como a regra supunha e eu não afirmava.**

#### A regra que impede contar essa ausência como saída tem agora um balanço

| | |
|---|---|
| Ausências registradas em Venda Online | **11** |
| Lotes distintos envolvidos | **5** |
| Desses cinco, quantos estão na lista hoje | **5** |
| Saídas reais em Venda Online em toda a série | **zero** |

**Onze ausências, nenhuma saída.** Se a regra não existisse, o histórico teria
onze saídas falsas — e cada uma delas contaminaria a estatística de piso de
arremate, que é justamente o número que calibra lance futuro. A regra nasceu de
uma retratação em 02/10/2026, por um único caso; hoje tem onze.

#### E a ausência não é aleatória no tempo: ela tem hora

Contadas as onze pelo horário da rodada em que ocorreram:

| Rodada | Ausências |
|---|---|
| 19h | **10** |
| 07h | 1 |

As coletas estão perfeitamente equilibradas — **sessenta e sete rodadas às 07h e
sessenta e sete às 19h** —, de modo que não há viés de amostragem a invocar. Se o
horário fosse irrelevante, a probabilidade de dez ou mais das onze caírem na
rodada da noite seria de **0,59%**.

**A conclusão é sobre o portal, não sobre o mercado: a busca da noite omite lote
de Venda Online com frequência que a da manhã não tem.** Isto deixa de ser
ambiguidade e passa a ser defeito conhecido, com assinatura horária — e lote de
Venda Online ausente numa rodada das 19h deve ser lido, por padrão, como falha de
listagem.

#### Duas retificações que esta rodada impõe

**A primeira, minha, de ontem.** Escrevi que o degrau de −2,50% do lote do
Estreito havia sido seguido da saída do lote, e que por isso a hipótese de
degraus repetidos "perdeu apoio". **O lote não saiu: oscilou, e está na lista
hoje, ao preço reduzido.** A ressalva que fiz era prudente na forma — registrei
que com uma observação não se distingue —, mas a premissa de fato que a motivou
era falsa. **Retiro-a.** O estado da questão volta a ser o de 23/11: um degrau
observado, cadência desconhecida. O que não muda, e não dependia disso, é que a
espera não serve de alavanca.

**A segunda, de método, e vale mais que a primeira.** Tentei construir um
controle melhor que a quarentena: consultar diretamente a página de detalhe do
lote ausente, para saber se ele ainda existe no sistema. **Não funciona, e fica
registrado para que ninguém volte a tentar.** O endpoint de detalhe só devolve a
ficha quando a busca da cidade, na mesma sessão, registrou aquele lote; consultado
isoladamente, devolve a página genérica de 25 KB, igual para lote existente e para
lote que saiu de verdade — testei com os dois casos e os resultados são
indistinguíveis. **Quer dizer: o portal não tem consulta por identificador
independente da busca, e por isso ausência na busca é a única informação
disponível.** A quarentena não é um paliativo à espera de instrumento melhor; é o
instrumento.

**O estoque:** dez aprovados na triagem, todos em Leilão SFI, todos reprovando na
margem; nenhuma alteração de preço; nenhuma saída. Comparáveis de mercado com
**sessenta e três dias** e nova recusa da fonte com HTTP 403.

### A reoferta mediu-se pela quinta vez, e o degrau de ontem ficou sem lote — 24/11/2026, 19h

Coleta íntegra: 20 lotes em Palhoça, 25 no 2º anel, 45 no total. A rodada traz
uma confirmação forte, um fato que enfraquece uma leitura minha de ontem e uma
anomalia que exige a próxima rodada para se resolver.

**A saída do lote de Aririú da Formiga confirmou-se**, por segunda ausência
consecutiva, e o controle novo anunciou-a com a relação medida: `+1 dia do 1º
certame (23/11/2026) — curso esperado`. É a vigésima segunda saída da série.

#### A confirmação: a escada da reoferta, pela quinta vez e com o mesmo fator

Voltou à lista o lote `144442332474-0` — **casa de 71,43 m² em Potecas, São
José**, que havia saído em **25/09/2026** após Leilão SFI negativo. Sessenta dias
depois, reaparece em **Licitação Aberta**, com certame em **09/12/2026**:

| | Preço | Avaliação | Fator | Desconto |
|---|---|---|---|---|
| Leilão SFI, até 25/09 | R$ 337.393,03 | R$ 360.000,00 | **0,937203** | 6,28% |
| Licitação Aberta, 24/11 | R$ 229.433,15 | R$ 360.000,00 | **0,637314** | **36,27%** |

A queda é de **−32,00%** — e **o fator novo é 0,637314, idêntico à sexta decimal
ao de outros seis lotes** de editais, cidades e tipos distintos. Contadas todas
as coletas da série, o fator aparece agora em **sete lotes distintos**; o
0,583884 em três; e o piso de **0,600000 em trinta e um**. A tabela de 19/11
media o estoque de então; esta contagem é de toda a série, e por isso os números
são maiores.

E o caso explica o mecanismo melhor do que qualquer um até aqui, porque mostra os
dois termos ao mesmo tempo. No Leilão SFI o preço estava a **93,72% da
avaliação**, pois o piso do 2º leilão é a dívida consolidada (art. 27, §2º, II,
da Lei 9.514/1997). Fracassado o certame, o imóvel passa ao ativo da Caixa e é
reofertado **com referência na avaliação**, no fator tabelado. **Os 32% de queda
não são desconto concedido: são a diferença entre a dívida de um devedor e a
tabela do vendedor.** Daí não haver relação entre o tamanho da queda e a
atratividade do lote — a queda mede o endividamento anterior, não o valor.

#### O fato que enfraquece a leitura de ontem, e é meu dever registrá-lo

Ontem apresentei o degrau de −2,50% do lote `000001028634-4` (comercial no
Estreito) como "o mecanismo pelo qual a espera produziria desconto", e calculei
que dezesseis degraus levariam dois anos e oito meses. **Hoje, doze horas
depois, esse lote saiu da lista.**

A aritmética continua correta; **a premissa dela, não.** Eu supus que o degrau
fosse a primeira parcela de uma série aplicada a um lote que permanece anunciado.
O que se observou foi outra coisa: o degrau veio, e em seguida o lote saiu. Pode
ter sido redução para fechar a venda — e então o degrau é ato final, não
periodicidade. Pode ser coincidência de um caso. **Com uma observação, não se
distingue.** Fica dito com clareza: **o cálculo dos dois anos e oito meses
pressupõe degraus que se repetem, e essa hipótese perdeu apoio em vez de
ganhar.** A conclusão prática não muda — a espera não é alavanca —, mas por razão
mais forte, não mais fraca.

#### A anomalia: a Venda Online esvaziou-se em doze horas

| Modalidade | Rodada das 07h | Rodada das 19h |
|---|---|---|
| Leilão SFI | 40 | 40 |
| Licitação Aberta | 3 | **4** |
| Venda Online | **4** | **1** |

Saíram, na mesma rodada, **três dos quatro lotes em Venda Online**: o comercial
do Estreito, o terreno `144440331727-7` da Fazenda Santo Antônio e o apartamento
`160000016077-0` de Areias. Nenhum conta como saída confirmada — Venda Online não
tem certame, e a regra os manda para `ausencias-venda-online.csv`.

**Três vendas em doze horas, numa modalidade que levou dois meses para mover um
preço, é a explicação menos provável.** Mais provável é comportamento do portal
ou migração de lote entre editais. Mas não se afirma o que não se mediu, e aqui
a medição é a próxima rodada: **se os três reaparecerem, foi oscilação; se os
três permanecerem fora, houve ato do vendedor — e aí a pergunta passa a ser qual.**

**O estoque:** dez aprovados na triagem, todos em Leilão SFI, todos reprovando
na margem. Comparáveis de mercado com **sessenta e dois dias** e nova recusa da
fonte com HTTP 403.

### A saída tem hora marcada, e ela é o dia seguinte ao certame — 24/11/2026

Coleta íntegra: 20 lotes em Palhoça, 27 no 2º anel, 47 no total. Dois movimentos,
e os dois confirmam regras — um de modo tão pontual que permitiu medir uma
regularidade que eu vinha registrando sem ter contado.

**O lote `844442969692-3` saiu da lista.** Apartamento de 45,82 m² na Rua
Natalino Campos Schaimann, 1150, Aririú da Formiga, Palhoça — Licitação Aberta,
R$ 142.037,17 contra avaliação de R$ 235.000,00, 39,56% de desconto. Era o
**primeiro colocado da triagem de ontem**, com prioridade 60,7. **Seu certame
foi em 23/11, ontem; a ausência é de hoje.**

**O lote `000001015918-6` voltou**, pelo preço idêntico, como Venda Online — o
terreno da Fazenda Santo Antônio que havia desaparecido na rodada de ontem. A
regra que o manteve fora do histórico de saídas provou-se em doze horas: Venda
Online não tem certame, ausência sem data marcada não é saída, e supor arremate
ali teria sido erro registrado em arquivo permanente.

#### A regularidade, agora contada e não apenas notada

Classifiquei as vinte e uma saídas confirmadas pela data do certame, e o
resultado é mais nítido do que eu supunha:

| Relação entre a saída e o certame | Casos |
|---|---|
| **Depois** do certame | **19 de 21** |
| Antes de todo certame | 2 de 21 |

E o intervalo não é difuso — ele se agrupa por modalidade:

| Modalidade | Intervalo entre o certame e a saída | Casos |
|---|---|---|
| Leilão SFI (dois certames) | **+5 a +7 dias** do 1º leilão, isto é, depois do 2º | 15 |
| Licitação Aberta (certame único) | **+1 dia**, exatamente | **5 de 5** |

Os cinco casos de Licitação Aberta — 30/09, 30/10, 05/11, 13/11 e o de hoje —
caem todos em `+1`, sem uma exceção. **A saída do lote em Licitação Aberta não é
evento aleatório: é o dia seguinte ao certame.** Serve de calendário, e serve de
alarme: lote de Licitação Aberta que *continua* na lista dois dias após o
certame é anomalia que merece ser olhada.

#### Mas sair no dia seguinte não quer dizer vendido

Fui ver o que houve depois de cada uma das quatro saídas anteriores de Licitação
Aberta, e aqui a amostra ainda é pequena e deve ser tratada como tal:

| Lote | Saiu | O que houve depois |
|---|---|---|
| `844442822457-2` | 30/09 | não voltou em 55 dias |
| `144442282177-5` | 30/10 | não voltou em 25 dias |
| `844441802944-0` | 05/11 | não voltou em 19 dias |
| `000001015918-6` | 13/11 | **voltou em 5 dias, como Venda Online** |

Três de quatro não voltaram; um voltou, e rápido, descendo a escada de
modalidades. **A ausência de `+1 dia` significa que o certame encerrou aquela
etapa — não que houve arremate.** O desfecho só se conhece depois: se o lote
volta em Venda Online, o certame fracassou; se não volta, provavelmente vendeu.

**Previsão registrada, para ser cobrada.** O lote de Aririú da Formiga ou
permanece fora — e então o certame de 23/11 o resolveu — ou reaparece em Venda
Online até cerca de **29/11/2026**, cinco dias, que é o único prazo de retorno
já observado nesta modalidade. A regra das duas rodadas o mantém em quarentena
até lá, e não registro saída confirmada antes disso. São oito previsões feitas
nesta série; sete foram confirmadas e esta é a oitava em aberto.

#### Nenhuma oportunidade se perdeu, e isto também se mede

Como o lote que saiu era o primeiro da triagem, cabe dizer com números se a
praça perdeu algo. **Não perdeu.**

| | Valor |
|---|---|
| Preço pedido | R$ 142.037,17 |
| VVR (45,82 m² × R$ 5.913 × 0,88) | R$ 238.421,62 |
| CTA | R$ 217.813,59 |
| **Margem sobre o CTA** | **2,89%** |
| Lance máximo para margem de 25% | R$ 106.762 |
| Lance máximo pelo capital disponível | R$ 34.149 |

Reprovava por margem com folga de vinte e dois pontos, e estava quatro vezes
acima do que o caixa alcança. **A primeira colocação na triagem media
atratividade bruta — desconto, bairro, tipologia —, não viabilidade.** Vale
reter a distinção: a triagem ordena candidatos, a viabilidade decide. Confundir
as duas é tomar a fila pela aprovação.

**O estoque remanescente:** dez aprovados na triagem, todos em Leilão SFI, todos
reprovando na margem; nenhum lote novo; comparáveis de mercado com **sessenta e
dois dias**, e a renovação barrada outra vez com HTTP 403.

### O vendedor baixa o preço de quem fica, e agora se sabe o passo — 23/11/2026

O portal voltou a responder nesta noite e a varredura das 19h foi coletada
integralmente: 21 lotes em Palhoça, 26 no 2º anel, 47 no total. O movimento da
rodada é pequeno em quantidade e grande em consequência.

**Um só lote mudou de preço, e é o primeiro caso de uma espécie nova.** O lote
`000001028634-4` — imóvel comercial de 577,10 m² na Av. Gov. Ivo Silveira, 2487,
Estreito, Florianópolis, em Venda Online — baixou de R$ 1.934.248,90 para
R$ 1.885.892,67.

| | Preço | Fator preço/avaliação | Desconto |
|---|---|---|---|
| Até 22/11 | R$ 1.934.248,90 | **0,637314** | 36,27% |
| Desde 23/11 | R$ 1.885.892,67 | **0,621381** | 37,86% |

A queda é de **exatamente −2,50%**: 1.934.248,90 × 0,975 = 1.885.892,6775, que
truncado ao centavo dá o valor publicado. E o fator novo é o antigo multiplicado
pelo mesmo 0,975 — isto é, **a Caixa não reprecificou o imóvel: aplicou um
desconto redondo sobre o preço tabelado anterior.** É mais uma confirmação de
que o fator 0,637314 é parâmetro administrativo, e não avaliação de mercado.

#### Por que este caso é de espécie diferente dos anteriores

Todas as quedas registradas até hoje — as de 22,67% e 63,13% em 19/11, a de
2,69% em 13/11 — eram de **reoferta**: o lote sai da lista, fracassa o certame e
volta sob outra modalidade, com outra referência de preço. Esta não. **O lote
não saiu, não trocou de modalidade e não mudou de edital. O vendedor
simplesmente baixou o preço de quem continua anunciado.**

A distinção não é acadêmica: confundir as duas coisas superestimaria
grosseiramente o desconto que a espera produz.

#### O passo e a cadência, que é o número que importa

O lote está na lista desde **23/09/2026** e foi observado **120 vezes**. Em cento
e dezenove dessas observações o preço foi o mesmo. **Ficou sessenta e um dias
parado e então desceu um degrau de 2,5%.**

É uma única observação, e eu não afirmo periodicidade a partir dela — não sei se
o próximo degrau vem em sessenta dias, em cento e vinte ou nunca. O que sei é o
limite: **nesta praça, em sessenta dias de observação contínua, um lote desceu um
degrau de 2,5% e nenhum outro desceu nenhum.**

E esse limite basta para responder à pergunta que a senhora tem em mãos. Para
levar o desconto dos 41,61% hoje disponíveis aos **61,0% que o mandato exige**,
seriam necessários **dezesseis degraus** de 2,5% (0,583884 × 0,975¹⁶ = 0,390 —
60,98% de desconto). A dezesseis degraus de sessenta e um dias, isso são
**novecentos e setenta e seis dias: dois anos e oito meses.**

**A conclusão de 19/11 não se retifica: reforça-se, e agora com a taxa medida.**
Escrevi então que a distância de 19,4 pontos "não se fecha esperando". O degrau
descoberto hoje é justamente o mecanismo pelo qual a espera produziria desconto —
e ele é lento demais para servir de alavanca. Restam as três de 06/10: **a margem
exigida, os custos fixos e o capital.**

#### Controle criado, para que não dependa de eu reparar

Achei este degrau por comparação manual das duas coletas, e isso é frágil: se o
movimento tivesse ocorrido numa rodada mais cheia, teria passado em branco. O
`scripts/degraus.py` passou a varrer todas as coletas gravadas e a registrar em
`dados/degraus-preco.csv` toda variação de preço de lote que **permaneceu** na
lista sob a **mesma modalidade**, com os dias que o preço anterior durou.
Rodado retroativamente sobre as 133 coletas, encontrou **um único** caso: este.
Os de reoferta ele exclui por construção, e continuam no `retornos.csv`, onde
pertencem.

#### O estoque, e a saída da rodada

Saiu da lista o terreno `000001015918-6` da Fazenda Santo Antônio, em São José —
o mesmo que em 18/11 havia descido a escada até Venda Online. **Não conta como
saída confirmada**, pela regra: Venda Online não tem certame, e ausência de lote
sem data marcada vai para `ausencias-venda-online.csv`, não para o histórico.
Pode ter sido proposta aceita, pode ser oscilação do portal. Não se supõe.

Nenhum lote novo. Os onze aprovados na triagem são os mesmos, todos reprovam na
margem, e a referência de mercado completa **sessenta e um dias** congelada —
a renovação dos comparáveis falhou outra vez, com o mesmo HTTP 403 e a mesma
página de desafio.

### Segunda rodada perdida, agora com a causa identificada — 23/11/2026

A varredura das 07h de 23/11 **também não foi entregue**. É a segunda rodada
consecutiva sem coleta, e desta vez a causa tem nome e código de estado.

Medido nesta manhã, com o tempo-limite da requisição elevado a 180 segundos para
que a falha pudesse ser vista por inteiro:

| Endereço | Resultado |
|---|---|
| `busca-imovel.asp` (página estática) | **HTTP 200**, 64.981 bytes em 42 s |
| `carregaPesquisaImoveis.asp` (busca por cidade) | **HTTP 504** aos 120 s |
| `detalhe-imovel.asp` (ficha do lote) | **HTTP 504** aos 120 s |

O corpo das duas respostas de erro é a página padrão da **Azion**, a borda que
serve o portal da Caixa, com o título *Server Error*. A leitura é direta: **a
borda responde, o servidor de origem da Caixa não.** As páginas estáticas saem
do cache da borda e por isso ainda chegam; tudo que depende de consulta ao
sistema da Caixa expira. Não é bloqueio antirrobô, não é lentidão do ambiente e
não é defeito do coletor — é indisponibilidade do originador, e nada que se faça
daqui a contorna.

**Dois defeitos meus que esta medição revelou, ambos corrigidos.**

O primeiro é de tempo-limite. O coletor desistia aos **60 segundos**, enquanto a
própria borda do portal só desiste aos 120 — e uma página simples levou 42 s
nesta manhã. O limite de 60 s classificava como falha o que por vezes era apenas
lentidão. Passou para 120 s.

O segundo é mais grave, e é de aderência outra vez. O coletor aceitava como boa
qualquer resposta com mais de 50 caracteres que não fosse redirecionamento. **A
página de erro da Azion tem 10.430 bytes** — passaria nesse teste e seria lida
como se fosse a ficha do imóvel, produzindo um lote de campos vazios em vez de
uma falha declarada. O defeito nunca se manifestou porque até ontem o portal
devolvia *nada* em vez de *outra coisa*; bastava o modo de falha mudar para que
o coletor mentisse em silêncio. Agora ele reconhece a página de erro pelo que
ela é e recusa-a.

**A lição, que é a mesma da banda de área e a mesma do lote do Roçado.** Um teste
de validade que pergunta *"veio alguma coisa?"* não responde *"veio a coisa
certa?"*. Em perícia é o vício de aceitar um documento porque ele existe, sem
conferir se é o documento pedido. **Todo controle de entrada deve verificar
identidade, não apenas presença.**

**Nada se conclui sobre a praça.** O último retrato é o das 07h de 22/11; a
próxima coleta que vingar comparará com ele, e o intervalo, já de vinte e quatro
horas, segue crescendo. Há um certame em **04/12** no horizonte, e a janela de
observação até lá está sendo consumida por indisponibilidade da fonte.

### A rodada que não houve, e o que a medição mostrou — 22/11/2026

A varredura das 19h de 22/11 **não foi entregue**. Não há planilha dessa rodada,
e o registro disto é parte do método: rodada sem coleta não se preenche com a
coleta anterior.

O portal não estava fora do ar — estava inutilizável, e a diferença se mediu:

| Operação | Tempo normal | Tempo em 22/11 à noite | Resultado |
|---|---|---|---|
| Busca da cidade (Palhoça) | poucos segundos | **370 s**, em duas voltas | 21 lotes listados |
| Uma página de detalhe | ~1 s | **1.055 s** (quatro tentativas) | **falhou** |

A busca devolveu a lista; **as páginas de detalhe não vieram**. A dezessete
minutos por lote e com quarenta e oito lotes, a coleta completa levaria cerca de
catorze horas — isto é, a rodada é impossível, não apenas lenta. O coletor agiu
como deve: não gravou nada, porque lista sem detalhe produziria linhas em branco
e o diff as leria como alteração do mercado.

**Nada se conclui sobre a praça a partir desta rodada.** O estoque pode ter
mudado entre a rodada das 07h e agora, e não se sabe; a próxima rodada comparará
com a das 07h de 22/11, e o intervalo de doze horas passa a vinte e quatro.

Registre-se, por fim, um erro meu de instrumentação que agravou o diagnóstico: a
coleta rodava com a saída canalizada por `grep`, que retém o texto em buffer
quando não escreve num terminal. Interrompido o processo, **o arquivo de saída
veio vazio** — e eu perdi a única prova de onde a coleta havia parado, tendo de
remedi-la com uma medição nova. A rotina passou a proibir o pipe na coleta em
segundo plano.

### O preço de reoferta é tabelado, e é isto que mede a distância até o mandato — 19/11/2026

Dois lotes voltaram à lista na mesma rodada, ambos saídos em 03/10 após Leilão
SFI, ambos reofertados em Licitação Aberta — e o controle criado na véspera os
apanhou sozinho, com a comparação pronta:

| Lote | Bairro | Preço antes | Preço agora | Queda |
|---|---|---|---|---|
| `144441764402-0` | Centro, Palhoça | R$ 477.998,55 | R$ 369.642,29 | **−22,67%** |
| `000001018127-9` | Kobrasol, São José | R$ 395.960,11 | R$ 145.971,08 | **−63,13%** |

A queda de 63% do lote de Kobrasol é a chave de tudo. **É o lote do desconto
negativo**, registrado em 03/10: a Caixa pedia R$ 395.960,11 por uma sala
avaliada em R$ 250.000,00 — 58,4% ACIMA da avaliação —, porque no 2º leilão do
SFI o piso é a dívida consolidada (art. 27, §2º, II, da Lei 9.514/1997), e não
um percentual da avaliação. Fracassado o SFI, o imóvel passa ao ativo da Caixa e
é reofertado **com referência na avaliação**. Daí a queda: não houve desconto
concedido, houve troca de referência.

**E a referência é tabelada.** Medindo preço ÷ avaliação em todo o estoque de
49 lotes, os números não se distribuem: eles se repetem, idênticos até a sexta
decimal, entre lotes de editais, cidades e tipos diferentes.

| Modalidade | Fator preço/avaliação | Desconto | Lotes |
|---|---|---|---|
| Leilão SFI | **0,600000** | 40,00% | 22 de 40 |
| Leilão SFI | acima de 0,60, até 1,0609 | 39% a **−6%** | 18 de 40 — piso pela dívida |
| Licitação Aberta / Venda Online | **0,637314** | 36,27% | 5 no estoque de 19/11 — **7 lotes em toda a série, contados em 24/11** |
| Licitação Aberta / Venda Online | **0,583884** | **41,61%** | 3 |
| Licitação Aberta | 0,604413 | 39,56% | 1 |

Os 0,600000 exatos em vinte e dois lotes são o piso do 2º leilão, a 60% da
avaliação. **Chamei-o de "piso legal" até 25/11/2026, e isto foi retificado**:
pela redação original do art. 27 da Lei 9.514/1997 o mínimo legal é a dívida, e
os 60% são piso comercial da Caixa quando a dívida é menor. Ver a seção de
25/11, que mede a regra inteira e consigna o que depende de texto legal a que
não tenho acesso. Os 0,583884 e 0,637314, repetidos a seis decimais em lotes sem
nenhuma relação entre si, **não são preço de mercado: são parâmetro
administrativo do vendedor.** Não arrisco a fórmula que os produz; registro o
fato, que é verificável e já se repetiu oito vezes.

#### A consequência, que é a mais importante de toda a série

O mandato, para uma unidade de 43,80 m² em Bela Vista avaliada em R$ 258.000,
admite lance de até R$ 100.541 — isto é, **exige 61,0% de desconto**. O melhor
que a reoferta já ofereceu é **41,61%**.

**A distância é de 19,4 pontos percentuais, e não se fecha esperando.** Esperar
o lote descer a escada das modalidades leva o desconto de 40% a 41,6%, não a
61%. Quem contava com a paciência como alavanca contava com o que esta praça não
dá — e isto agora está medido, não suposto.

Restam as três alavancas de 06/10, e só elas: **a margem exigida, os custos
fixos e o capital.** A quarta, que eu não havia descartado com números até hoje
— *aguardar a reoferta* —, está descartada.

#### Uma pergunta que é da senhora, não minha

O lote `144441764402-0` é um apartamento de **72,45 m² no Centro de Palhoça**, a
R$ 369.642,29 contra avaliação de R$ 580.000,00 — **36,3% de desconto**, em
Licitação Aberta com certame em 04/12. Está na cidade-alvo e **fora da lista de
bairros** do mandato, que nomeia Bela Vista, Pedra Branca, Passa Vinte, Aririú,
Jardim Eldorado, Ponte do Imaruim e Caminho Novo. A triagem o descarta por isso,
e corretamente — mas o descarte é de regra, não de mérito. **Incluir o Centro na
praça-alvo é decisão sua**, e enquanto não houver, não levanto comparáveis do
bairro nem o precifico: seria responder a uma pergunta que a senhora não fez.

### A escada da reoferta, e um erro meu que ela revelou — 18/11/2026

O lote **000001015918-6**, terreno da Fazenda Santo Antônio, cuja saída se
confirmou em 13/11 após Licitação Aberta negativa, voltou à lista em 18/11 —
**como Venda Online, pelo preço idêntico**. Comparadas as trinta e seis colunas
da coleta, mudaram seis, e todas pela mesma causa: caíram edital, leiloeiro,
plataforma e data de certame, e a modalidade passou de Licitação Aberta a Venda
Online. Preço, avaliação, área e regras de condomínio, financiamento e FGTS:
**idênticos**.

Fui então cruzar todo o estoque já coletado com o histórico, e o levantamento
produziu duas coisas: uma constatação e uma retificação.

**A constatação — a Caixa desce uma escada de modalidades.** Dos sessenta e três
lotes distintos vistos até aqui, dois mudaram de modalidade, e os três retornos
registrados formam uma sequência coerente:

| Retorno | Lote | Antes | Depois | Preço | Variação |
|---|---|---|---|---|---|
| 11/11 | `878771588251-5`, Bela Vista | Leilão SFI | Leilão SFI (edital novo) | R$ 168.933 → R$ 169.635 | **+0,42%** |
| 13/11 | `855551517677-2`, Roçado | Leilão SFI | **Licitação Aberta** | R$ 279.000 → R$ 271.506 | **−2,69%** |
| 18/11 | `000001015918-6`, Fazenda Santo Antônio | Licitação Aberta | **Venda Online** | R$ 1.470.221 → R$ 1.470.221 | **0,00%** |

A escada é **Leilão SFI → Licitação Aberta → Venda Online**, e ela muda o regime
de acesso: a Venda Online aceita proposta a qualquer momento, sem certame, sem
habilitação prévia em plataforma de leiloeiro e sem a corrida de um dia marcado.

> **Retificado em 19/11/2026.** Escrevi aqui que a reoferta "não oferece
> desconto", porque nos três primeiros casos a maior queda havia sido de 2,69%.
> **Estava errado, e o erro era de amostra pequena.** Dois retornos de 19/11
> caíram 22,67% e 63,13%. A reoferta oferece desconto, e grande; a seção de
> 19/11 explica por quê e quanto.

**A retificação.** Em 13/11 anunciei o lote do Roçado como **lote novo**. Não
era: havia saído em 19/09, como Leilão SFI, e voltava cinquenta e cinco dias
depois sob outra modalidade. O dado para desfazer o engano estava no próprio
repositório — o histórico de saídas — e eu não o consultei, dois dias depois de
ter escrito, a propósito do lote de Bela Vista, que *sair da lista não é estado
permanente*. **Enunciar a regra não é aplicá-la**, e a diferença entre as duas
coisas é um controle automático.

**Controle criado, para que não dependa de mim.** O `historico.py` passou a
cruzar todo lote que aparece com o histórico de saídas e a anunciar o retorno
como retorno, com a comparação de modalidade e de preço, registrando-o em
`dados/retornos.csv`. Rodado retroativamente, recuperou os três casos. O
`panorama.py`, pelo mesmo motivo, passou a contar cada lote pela versão **mais
recente** e não pela primeira: contado pela primeira, o terreno seguiria somando
na coluna da Licitação Aberta, numa tabela que existe para dizer o que a
modalidade determina **hoje**.

### O R$/m² depende da banda de área, e a banda grande vale menos — 23/10/2026

O edital **0056/0226 - CPA/RE** trouxe, na rodada das 19h, o primeiro lote de
Bela Vista com área acima de 50 m²: **844440215690-1**, apartamento de
**55,98 m²**, avaliação de R$ 240.000, pedido de **R$ 144.000** — 40% de desconto
anunciado, certames em 14/12 e 17/12.

Ao precificá-lo, deparei-me com uma questão de método que até aqui não se havia
apresentado: **o levantamento de comparáveis foi pesquisado na banda de 42 a
49 m²**, porque toda a amostra anterior cabia nela. Aplicar aquele R$/m² a uma
unidade de 55,98 m² seria extrapolar a banda pesquisada. Fui ao arquivo de 23/09
conferir o que ele próprio contém, e a resposta estava lá:

| Banda de área | Anúncios | R$/m² mediano | Preço mediano |
|---|---|---|---|
| 42 a 49 m² | 13 | **R$ 5.913** | R$ 270.000 |
| 50 a 62 m² | 12 | **R$ 5.333** | R$ 280.000 |

**A unidade maior vende por 9,8% menos por metro quadrado.** O preço total sobe —
de R$ 270 mil para R$ 280 mil —, mas não na proporção da área: é o padrão
conhecido de que o metro marginal vale menos que o primeiro. O levantamento de
23/09 já sustentava as duas bandas; o que faltava era a pergunta.

**O efeito sobre este lote é decisivo, e não cosmético:**

| R$/m² aplicado | VVR | Margem | Teto do mandato | Distância até o pedido |
|---|---|---|---|---|
| R$ 5.913 (banda errada) | R$ 291.288 | 23,0% | R$ 140.799 | R$ 3.201 — **2,2%** |
| R$ 5.333 (banda correta) | R$ 262.716 | **9,0%** | R$ 118.375 | R$ 25.625 — **17,8%** |

Pela banda errada, o lote **aparentaria faltar 2,2% para passar** — o mais perto
que qualquer lote desta praça jamais chegou, e provavelmente bastaria para
justificar diligência, visita e proposta. Pela banda correta, falta 17,8%, e o
lote reprova com folga. **Quatorze pontos de margem dependiam de qual coluna da
mesma planilha se consultava.**

**Correção aplicada ao instrumento, não apenas ao laudo.** O `planilha.py` passou
a ter duas premissas de R$/m², uma por banda, e escolhe a do lote pela área na
montagem da aba — de modo que a conta não dependa de quem a faz lembrar da
banda. A escolha fica explícita na célula e continua recalculando quando a
senhora editar a premissa.

**A lição de método.** O erro que quase cometi não é de cálculo nem de fonte: é
de **aderência da amostra ao objeto**. A mediana de R$ 5.913 era correta, apurada
e recente o bastante; apenas não se referia a este imóvel. Em perícia é o mesmo
vício de tomar laudo de imóvel semelhante por laudo do imóvel periciado — o
número está certo e responde a outra pergunta. **Antes de aplicar uma mediana,
verifique-se de que o objeto pertence à população de onde ela saiu.**

### O teto de lance do mandato, por metro quadrado — e a distância até o piso da Caixa

Apurado em 06/10/2026, quando três editais novos (0050, 0051 e 0052 — CPA/RE)
trouxeram dois lotes inéditos em Bela Vista e permitiram, pela primeira vez,
comparar unidades do mesmo bairro com metragens diferentes.

Com as premissas vigentes e o R$/m² de mercado em R$ 5.913, o lance máximo que
cumpre o mandato é este:

| Área privativa | Lance para margem de 25% | R$/m² | Lance de equilíbrio (margem zero) | R$/m² |
|---|---|---|---|---|
| 43,80 m² | R$ 100.541 | **R$ 2.295** | R$ 139.778 | R$ 3.191 |
| 48,49 m² | R$ 114.985 | **R$ 2.371** | R$ 158.423 | R$ 3.267 |
| 52,85 m² | R$ 128.412 | **R$ 2.430** | R$ 175.757 | R$ 3.326 |
| 60,00 m² | R$ 150.432 | **R$ 2.507** | R$ 204.181 | R$ 3.403 |

O teto por metro quadrado **sobe com a área**, porque os custos fixos da operação
— dívidas, desocupação, carrego — se diluem em mais metros. Unidade pequena é
penalizada por aritmética, não por mercado.

#### A constatação que isto produz, e que é estrutural

O piso do 2º leilão em Bela Vista, a 60% da avaliação, equivale a cerca de
**R$ 3.452/m²** nas unidades de 43,80 m². O teto do mandato, para a mesma área, é
**R$ 2.295/m²**. **A Caixa pede 50% acima do que o mandato admite.**

Isso não é característica de um lote nem azar de uma rodada: é a relação entre o
piso de 60% praticado pela Caixa no 2º leilão e a margem exigida, nesta praça,
com estas premissas. (Em Bela Vista a dívida fica abaixo dos 60%, de modo que o
piso aplicável é **comercial**, não legal — retificado em 25/11/2026.)
Enquanto as três grandezas não mudarem, **nenhum lote de Bela Vista passará** —
e a varredura seguirá reprovando por aritmética, não por falta de oportunidade.

As três grandezas que poderiam mudar isso, nomeadas para que a decisão seja
consciente:

1. **A margem exigida.** Baixar de 25% para 15% elevaria o teto, sem eliminar a
   distância. É decisão de apetite, não de cálculo.
2. **Os custos fixos.** Condomínio atrasado (R$ 12.000) e desocupação
   (R$ 15.000) são estimativas de premissa, não valores apurados. Um lote com
   condomínio em dia e ocupante que desocupe sem ação muda o teto de modo
   relevante — e **só a due diligence apura isso**.
3. **O R$/m² de mercado**, congelado em 23/09 por bloqueio da fonte. Se o mercado
   real estiver acima de R$ 5.913, todo o quadro se desloca a favor; se estiver
   abaixo, contra. **É a maior incerteza aberta do acompanhamento.**

#### O primeiro lote com margem positiva de toda a série

O lote **878771176139-0** (Av. Paulo Roberto Vidal, 475, apto. 611, bl. A),
48,49 m² a R$ 153.000, apurou margem de **+2,6%** — a primeira positiva desde
16/09. Reprova no mandato, por estar muito abaixo dos 25%, e segue fora do
alcance do caixa; mas a causa do resultado é a lição que fica.

Os quatro lotes aprovados na triagem têm desconto declarado entre 34,5% e 40%, e
todos os quatro estão em Bela Vista. O que separa o de margem positiva dos de
margem negativa **não é o desconto, nem o preço absoluto**: é o preço por metro
quadrado de área privativa.

| Lote | Endereço | R$/m² de entrada | Margem |
|---|---|---|---|
| 878771176139-0 | Paulo Roberto Vidal, 475, ap. 611 | **R$ 3.155** | **+2,6%** |
| 878770561220-5 | Sebastião Alzemiro, 387, ap. 104 | R$ 3.452 | −5,5% |
| 878770638651-9 | Sebastião Alzemiro, 387, ap. 401 | R$ 3.452 | −5,5% |
| 878771588251-5 | Paulo Roberto Vidal, 2050, ap. 102 | R$ 3.857 | −12,9% |

**Regra de seleção que decorre disto:** ordenar candidatos por **preço por metro
quadrado de área privativa**, e não pelo desconto sobre a avaliação da Caixa. O
desconto mede a relação entre preço e avaliação — e a avaliação, como já
registrado em 03/10, acompanha a dívida consolidada, não o valor do imóvel. O
preço por metro quadrado mede a relação entre o que se paga e o que se vai
vender. É a única das duas que informa a margem.

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

**O remédio do navegador foi testado em 05/10/2026 e não funciona aqui.** Fica
registrado o diagnóstico, para que ninguém volte a gastar tempo com ele sem
antes mudar a configuração do ambiente.

O que se fez: instalou-se o Playwright, apontou-se o Chromium do ambiente e
autorizou-se exclusivamente a chave do CA do proxy da sessão, por fixação de
SPKI — sem desligar a verificação de TLS, que permanece recusando qualquer
outro certificado inválido. O navegador passou a dialogar com a fonte de fato:
a resposta deixou de ser erro de certificado e passou a ser uma página real de
31 KB.

Onde parou: a página é o desafio do Cloudflare, e o texto dela próprio diz a
causa — *"as configurações de internet ou firewall bloquearam o acesso do seu
dispositivo a challenges.cloudflare.com"*. Esse é o host que executa a
verificação. A política de rede do ambiente **não o permite** e responde 403 à
tentativa de conexão. **O desafio não pode ser resolvido porque o verificador
não pode ser carregado** — e isso nenhum navegador contorna.

Testadas na mesma data, todas barradas: `imoveis-sc.com.br`, `vivareal.com.br` e
`zapimoveis.com.br` com 403 de antirrobô; `chavesnamao.com.br`, `olx.com.br`,
`imovelweb.com.br` e `quintoandar.com.br` sem completar conexão.

**O que destravaria:** acrescentar `challenges.cloudflare.com` — e o domínio da
fonte escolhida — aos domínios permitidos do ambiente, em Network access, pela
opção Custom, preservando a lista padrão dos gerenciadores de pacote
(`code.claude.com/docs/en/cloud-environments#network-access`). A alteração só
vale em **sessão nova**. É decisão da investidora, mas agora com o custo
conhecido: uma configuração, não um desenvolvimento.

**Nota de método, porque houve erro meu no caminho.** O diagnóstico do proxy
exibe `"selective": false`, e eu o li como ausência de lista de domínios
permitidos — cheguei a afirmar à investidora que o bloqueio era só dos sites.
A primeira tentativa de sair para um host não previsto desmentiu-me: *"Host not
in allowlist"*. **A lista existe.** O campo do diagnóstico não significava o que
supus, e a lição é que configuração se comprova por tentativa de uso, nunca por
leitura de um campo de estado.

#### Fontes de preço FECHADO: tentadas em 12/10/2026, nenhuma disponível

Com a referência de mercado congelada há dezenove dias, tentei a via que este
perfil sempre apontou como superior — **preço de transação, não preço pedido**.
O resultado, para que não se repita o esforço:

| Fonte | Resultado | Natureza do obstáculo |
|---|---|---|
| `servicodados.ibge.gov.br` | 403 no CONNECT | **política de rede** do ambiente |
| `servicos.ibge.gov.br` | 403 no CONNECT | **política de rede** |
| `dados.gov.br` | 403 no CONNECT | **política de rede** |
| `gov.br/receitafederal` | 403 no CONNECT | **política de rede** |
| `sinapi.caixa.gov.br` | HTTP 504 | indisponibilidade do servidor |
| `www.palhoca.sc.gov.br` | falha de validação TLS | certificado não confere com o nome do host |

Os quatro primeiros são **negativas de política** — não se insiste nelas, e o
remédio é o mesmo dos comparáveis: acrescentar o domínio aos permitidos do
ambiente, em sessão nova. O último é defeito de certificado, e **não se
contorna desligando a verificação de TLS**, em nenhuma hipótese.

**Ressalva de expectativa, para não criar ilusão:** mesmo liberado o acesso, é
incerto que a Prefeitura de Palhoça publique microdados de ITBI. Muitos
municípios divulgam apenas a planta genérica de valores, que é referência
fiscal e **não** preço de transação. A via vale ser tentada, não vale ser
contada como resolvida.

### A revisar

- Locação: nenhuma fonte liberada na política de rede entrega anúncios de
  aluguel do bairro. Sem isso não há cap rate nem plano B de renda enquanto o
  flip não sai.
- Os comparáveis são anúncios, não transações. Preço fechado exigiria ITBI da
  Prefeitura de Palhoça ou consulta a corretor local.
