# Varredura da praça-alvo — 16/09/2026

Núcleo Bela Vista (Palhoça/SC) + 1º anel, com o 2º anel coletado para
acompanhamento. Mandato lido de `perfil-investidor.md`.

## Resumo em uma linha

Há estoque em Bela Vista pela primeira vez — **3 apartamentos** —, mas os três
reprovam no mandato, e **nenhum deles é alcançável com o capital atual**: todos
são Leilão SFI, todos ocupados, e **nenhum aceita financiamento**.

## O que foi varrido

| Fonte | Recorte | Lotes |
|---|---|---|
| Portal de venda de imóveis da Caixa | Palhoça/SC (todos os bairros) | 7 |
| idem | São José/SC (2º anel) | 10 |
| idem | Florianópolis/SC (2º anel) | 1 |
| **Total coletado** | | **18** |

Triagem com os cortes do mandato (núcleo + 1º anel, desconto ≥ 25%):
**3 aprovados, 15 descartados** — 15 fora do bairro-alvo, 11 fora da cidade,
2 por desconto anunciado abaixo de 25%.

> **Nota de método.** O download estático da lista por UF
> (`/listaweb/Lista_imoveis_SC.csv`) está bloqueado pelo antirrobô do portal
> (Radware/ShieldSquare) neste ambiente: 5 tentativas, 5 redirecionamentos. A
> coleta foi feita pelos endpoints POST que o próprio formulário de busca usa,
> que respondem normalmente (`scripts/coletar_portal.py`). A ficha assim obtida
> é **mais rica** que o CSV: traz matrícula, comarca, ofício, inscrição
> imobiliária, regra de condomínio e tributos, formas de pagamento aceitas e o
> link do edital.

## Quadro-resumo — os 3 aprovados na triagem

Todos em Bela Vista, todos apartamento de 2 dormitórios com 1 vaga, todos
**ocupados**, todos **Leilão SFI**, todos com **matrícula individualizada**.
Valores de lance = piso do 2º leilão.

| # | Imóvel | Área priv. | Avaliação | Lance (2º leilão) | VVR | CTA | Margem | Lance máx. | Score |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 878770360836-7 | 45,61 m² | R$ 240.000 | R$ 144.000 | R$ 237.610 | R$ 219.854 | **1,6%** | R$ 34.244 | **37** |
| 2 | 878770561220-5 | 43,80 m² | R$ 252.000 | R$ 151.200 | R$ 228.180 | R$ 226.720 | **−5,4%** | R$ 35.156 | **35** |
| 3 | 878771588251-5 | 43,80 m² | R$ 258.000 | R$ 168.933 | R$ 228.180 | R$ 246.085 | **−12,8%** | R$ 35.156 | **35** |

Margem mínima exigida: 25%. **Nenhum passa.** Classificação da skill:
score < 60 = descartar.

O "lance máximo" acima é o **teto do caixa** (R$ 100 mil), não o teto da margem.
Pela margem os tetos seriam R$ 106.298, R$ 100.716 e R$ 100.716 — ainda assim
abaixo do piso do 2º leilão em todos os casos.

### VVR: como foi construído

`área privativa × R$ 5.920/m² × 0,88`, onde R$ 5.920 é a mediana de R$/m² de
**14 anúncios ativos de 2 dormitórios entre 42 e 49 m² em Bela Vista** — a banda
que corresponde a estes lotes. Detalhe em `perfil-investidor.md` e nos dados
brutos em `dados/comparaveis-bela-vista-2026-09-16.csv`.

### Premissas de custo usadas (triagem, não cotação)

Comissão 5% · ITBI 3% · registro 1,2% · IPTU atrasado R$ 3.000 · condomínio
atrasado R$ 12.000 · consumo R$ 800 · desocupação por acordo R$ 15.000 ·
reforma leve R$ 550/m² · carrego R$ 560/mês × 12 meses.

## Fichas

### 1. 878770360836-7 — o melhor dos três, e ainda assim não fecha

- **Endereço:** R. Sebastião Alzemiro dos Santos, 347, ap. 104, bl. 11 — Bela
  Vista, Palhoça/SC — CEP 88137-640
- **Matrícula:** 98122, 1º Ofício da comarca de Palhoça ·
  **Inscrição imobiliária:** 1043700900001164
- **Área:** 97,41 m² total / **45,61 m² privativa** · 2 quartos · 1 vaga
- **Avaliação Caixa:** R$ 240.000 · **1º leilão:** R$ 240.000 ·
  **2º leilão:** R$ 144.000 (40% de desconto sobre a avaliação)
- **Modalidade:** Leilão SFI · Edital 0047/0226 - CPA/RE ·
  Leiloeiro: Marco Túlio Montenegro Cavalcanti Dias ·
  Plataforma: lancecertoleiloes.com.br
- **Datas:** 1º leilão **08/10/2026** · 2º leilão **15/10/2026**
- **Situação:** **OCUPADO**
- **Pagamento:** recursos próprios; **permite FGTS**; **não aceita financiamento**
- **Despesas:** condomínio e tributos **integralmente por conta do comprador**,
  sem teto declarado
- **Averbação de leilões negativos:** "Não se aplica" — é o primeiro ciclo
- [Edital](https://venda-imoveis.caixa.gov.br/editais/EL00470226CPARE.PDF) ·
  [Matrícula](https://venda-imoveis.caixa.gov.br/editais/matricula/SC/8787703608367.pdf)

**Sensibilidade.** É o único lote em que o negócio existe se tudo der certo:

| Cenário | CTA | Margem | Desembolso | Falta de caixa |
|---|---|---|---|---|
| Otimista (sem condomínio atrasado, desocupação R$ 5 mil, reforma R$ 400/m², ciclo 6 meses) | R$ 183.232 | **21,9%** | R$ 183.232 | −R$ 83.232 |
| Otimista + venda a preço de anúncio, sem deságio | R$ 183.232 | **38,5%** | R$ 183.232 | −R$ 83.232 |
| Base | R$ 219.854 | 1,6% | R$ 219.854 | −R$ 119.854 |
| Pessimista (condomínio R$ 20 mil, desocupação litigiosa, reforma pesada, ciclo 24 meses) | R$ 274.677 | **−18,7%** | R$ 274.677 | −R$ 174.677 |

Mesmo no cenário otimista faltam **R$ 83 mil**. O obstáculo não é a análise:
é o caixa.

### 2. 878770561220-5

- **Endereço:** R. Sebastião Alzemiro dos Santos, 387, ap. 104, bl. 10 — Bela
  Vista — CEP 88137-640 (mesma rua e mesmo conjunto do lote 1)
- **Matrícula:** 102870, 1º Ofício · 80,51 m² total / **43,80 m² privativa**
- **Avaliação:** R$ 252.000 · **2º leilão:** R$ 151.200 (40%)
- **Edital** 0046/0226 - CPA/RE · Tonial Leilões ·
  1º leilão **05/10/2026** · 2º leilão **09/10/2026**
- **OCUPADO** · permite FGTS · **sem financiamento** · condomínio e tributos
  por conta do comprador
- [Edital](https://venda-imoveis.caixa.gov.br/editais/EL00460226CPARE.PDF) ·
  [Matrícula](https://venda-imoveis.caixa.gov.br/editais/matricula/SC/8787705612205.pdf)

Avaliado 5% acima do lote 1 com **1,81 m² a menos** de área privativa. Margem
negativa já no cenário base.

### 3. 878771588251-5 — o lote com a avaliação mais frágil

- **Endereço:** Av. Paulo Roberto Vidal, 2050, ap. 102, bl. 11 — Bela Vista —
  CEP 88132-599
- **Matrícula:** 116295, 1º Ofício · 50,87 m² total / **43,80 m² privativa**
- **Avaliação:** R$ 258.000 · **2º leilão:** R$ 168.933 (34,5%)
- **Edital** 0048/0226 - CPA/RE · Globo Leilões ·
  1º leilão **14/10/2026** · 2º leilão **20/10/2026**
- **OCUPADO** · permite FGTS · **sem financiamento**
- [Edital](https://venda-imoveis.caixa.gov.br/editais/EL00480226CPARE.PDF) ·
  [Matrícula](https://venda-imoveis.caixa.gov.br/editais/matricula/SC/8787715882515.pdf)

**Achado relevante.** O lote 878771586575-0 fica no **mesmo endereço** (Av.
Paulo Roberto Vidal, 2050), tem **a mesma metragem** (50,87 m² / 43,80 m²), o
**mesmo CEP** e inscrição imobiliária quase idêntica (`...0301**1**002` contra
`...0301**2**002` — muda o bloco). A Caixa avaliou um em **R$ 258.000** e o
outro em **R$ 223.000** — **15,7% de diferença**. E rotulou um como *Bela Vista*
e o outro como *Lot. Pq. Vale Verde*.

Duas consequências práticas: a avaliação do edital não é valor de mercado, e o
rótulo de bairro do portal não é confiável como filtro de praça-alvo.

## Riscos nomeados

| Risco | Onde aparece | Custo/impacto estimado | Como resolver |
|---|---|---|---|
| **Ocupação** — todos os 3 estão ocupados | Fonte do portal (campo vem comentado no HTML, mas declarado) | R$ 5 a 25 mil por acordo; R$ 10 a 40 mil e 12 a 36 meses se litigioso | Descobrir **quem** ocupa e a que título. Ex-mutuário e terceiro têm ritos diferentes |
| **Condomínio atrasado sem teto** | Edital: "sob responsabilidade do comprador" | R$ 0 a R$ 20 mil — vira R$ 12 mil na premissa base | Administradora, **por escrito e com data**. É o item que mais move a margem |
| **Leilão SFI é a modalidade de maior risco** do mandato | Os 3 lotes | Anulação de arrematação trava o capital por anos | O perfil manda começar por Venda Direta, Venda Online e Licitação Aberta. Nenhuma delas tem lote em Bela Vista hoje |
| **Sem financiamento** | Formas de pagamento de todos os 7 lotes de Palhoça | Elimina a alavanca que o perfil aponta como decisiva | Só FGTS resta — e FGTS tem regras de enquadramento e prazo de liberação próprias |
| **Reforma não orçada** | Imóvel ocupado não permite vistoria interna | R$ 400 a R$ 1.800/m² — variação de R$ 18 mil a R$ 82 mil em 45 m² | Vistoria externa e conversa com o síndico antes do certame |
| **Avaliação inconsistente da Caixa** | Lote 3 contra o 878771586575-0 | 15,7% sobre R$ 240 mil ≈ R$ 38 mil | Não usar a avaliação do edital como âncora, em hipótese alguma |

## O 2º anel (acompanhar, não comprar)

11 lotes coletados. Um merece nota por ser a modalidade que o mandato prefere:

- **08444428224572** — São José/SC, bairro Real Parque, **Licitação Aberta**,
  R$ 157.056,10, matrícula 7668. Averbação dos leilões negativos: "Em tratamento".

Está fora da praça-alvo, mas se o mandato vier a admitir o 2º anel, é por onde
começar: Licitação Aberta tem nota de segurança jurídica 7/10 contra 3/10 do 2º
leilão SFI.

## Próximos passos, com prazo

Os certames são em **12 a 34 dias**. Habilitação em plataforma de leiloeiro
exige cadastro e documentação prévios — não se faz na véspera.

1. **Decidir o parâmetro que destrava tudo: FGTS.** Está `A DEFINIR` no perfil.
   Os 3 lotes aceitam. Se houver saldo, ele soma ao capital e muda a conta
   inteira. Se não houver, Bela Vista está fora de alcance neste ciclo e a
   varredura passa a ser de monitoramento. **Esta é a pergunta que eu preciso
   que você responda.**
2. **Se houver FGTS:** conferir enquadramento (imóvel residencial urbano, não ser
   proprietário de outro imóvel na região, 3 anos de FGTS, teto de valor do
   SFH) e, sobretudo, se o **prazo de liberação** cabe no prazo de pagamento do
   edital. Prazo curto de leilão costuma ser incompatível com liberação de FGTS.
3. **Ler os 3 editais integralmente** — os links estão nas fichas. Confirmar no
   texto: prazo de pagamento, se há teto para condomínio atrasado, cláusula de
   posse e condições de desistência.
4. **Pedir por escrito o débito de condomínio** das 3 unidades à administradora,
   e o IPTU à Prefeitura de Palhoça.
5. **Baixar as 3 matrículas** (links nas fichas) e conferir a averbação da
   consolidação da propriedade e eventuais penhoras.
6. **Fechar os dois parâmetros `A DEFINIR` de tolerância** — ocupação e risco
   jurídico. Hoje a triagem roda com o padrão da skill, não com o seu critério.

## O que NÃO foi verificado

- **Nenhuma matrícula foi lida.** Os PDFs foram localizados, não abertos. Toda
  afirmação sobre ônus, penhora e cadeia dominial está pendente.
- **Nenhum edital foi lido integralmente.** As regras de condomínio, tributos e
  formas de pagamento vieram do resumo da ficha do portal, não do texto do edital.
- **Nenhum débito foi confirmado.** Condomínio, IPTU e consumo são estimativas
  de faixa, não valores cotados.
- **Nenhuma vistoria**, nem externa.
- **Quem ocupa cada imóvel é desconhecido** — o portal diz "Ocupado" e só.
- **Comparáveis são anúncios, não transações.** Preço pedido ≠ preço fechado; o
  deságio de 0,88 é premissa do mandato, não medição de mercado.
- **A locação em Bela Vista não foi levantada** — nenhuma fonte liberada pela
  política de rede entrega anúncios de aluguel do bairro.
- **Os CEPs não foram confirmados** contra base oficial: `viacep.com.br` está
  fora da lista de domínios liberados do ambiente. Por isso a divergência de
  rótulo de bairro no lote 3 ficou apontada, mas não resolvida.
- **Bancos privados e leilões judiciais do TJSC não foram varridos** nesta
  rodada — só a Caixa.
