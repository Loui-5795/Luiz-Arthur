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

Acumulado em `dados/historico-saidas.csv`. **Treze saídas** até 09/10/2026, em
doze Leilões SFI e uma Licitação Aberta. A décima terceira é a primeira
**verificada prospectivamente**: o lote de São Sebastião (`878771537674-1`,
R$ 186.000, 52,85 m²) teve 1º leilão em 02/10 e 2º em 08/10, permaneceu listado
entre as duas datas, e deixou a lista na manhã seguinte ao 2º — tudo anunciado
antes de ocorrer e conferido depois. O portal **não declara a causa**:
arremate, suspensão, retirada e purgação da mora são indistinguíveis daqui.

| Constatação | n | Situação |
|---|---|---|
| Nenhum lote saiu entre o 1º e o 2º leilão | 10 de 10 (dos que têm duas datas) | **mantida** |
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
piso legal do 2º leilão e a margem exigida, nesta praça, com estas premissas.
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

### A revisar

- Locação: nenhuma fonte liberada na política de rede entrega anúncios de
  aluguel do bairro. Sem isso não há cap rate nem plano B de renda enquanto o
  flip não sai.
- Os comparáveis são anúncios, não transações. Preço fechado exigiria ITBI da
  Prefeitura de Palhoça ou consulta a corretor local.
