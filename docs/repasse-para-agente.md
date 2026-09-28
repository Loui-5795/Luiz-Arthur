# Repasse — projeto de garimpo de imóveis em leilão

Documento de passagem de bastão. Escrito para que **outro agente de IA** assuma
este projeto sem repetir o que já foi descoberto, e para que não reintroduza os
defeitos que já foram corrigidos.

Data de corte: **28/09/2026**. Repositório: `Loui-5795/Luiz-Arthur`, branch
`claude/venda-imoveis-caixa-access-22lqqc`. 29 commits, 20 planilhas geradas,
12 dias de operação contínua.

Quem usa: **contadora e perita**, investidora pessoa física, sem experiência em
programação. Pediu escrita em português culto formal. Não lê código — lê
planilha e texto.

---

## 1. O que o projeto faz

Varre o estoque de imóveis retomados da Caixa duas vezes por dia, tria contra um
mandato de investimento escrito, precifica os sobreviventes e entrega uma
planilha `.xlsx` na conversa com a usuária.

O projeto **não lista leilões** — isso qualquer site faz. Ele separa oportunidade
real de armadilha, e o número que decide não é o desconto anunciado: é o **Custo
Total de Aquisição (CTA)** contra o **Valor de Venda Rápida (VVR)**.

### Os dois princípios que governam tudo

1. **Desconto não é lucro.** Um lote com 40% de desconto sobre uma avaliação que
   ninguém auditou, ocupado, com condomínio atrasado sem teto, é prejuízo.
2. **O edital manda.** Regra geral serve para triagem. Decisão de lance se toma
   lendo o edital daquele lote e a matrícula daquele imóvel. Quando não se leu,
   diz-se que não se leu.

---

## 2. O mandato

Fonte única: `perfil-investidor.md` na raiz. **Todo corte, score e critério lê
de lá.** Mudou a estratégia? Muda o arquivo, não os scripts.

| | |
|---|---|
| Praça-alvo (núcleo) | Palhoça/SC — bairro **Bela Vista** |
| 1º anel (entra na varredura) | Pedra Branca, Passa Vinte, Aririú, Jardim Eldorado, Ponte do Imaruim, Caminho Novo |
| 2º anel (só acompanhar) | São José e Florianópolis continental |
| Capital à vista | R$ 50.000 a R$ 100.000 |
| Tese de saída | Revenda (flip), ciclo de 6 a 12 meses |
| Margem líquida mínima | **25% sobre o CTA** |
| Desconto anunciado mínimo | 25% |
| Fator de deságio do VVR | 0,88 (venda em 90 dias) |
| Custo de venda | 6% de corretagem |

**Três parâmetros seguem `A DEFINIR`** e a varredura roda com o padrão da skill,
registrando a pendência: aceita financiamento, aceita FGTS, tolerância a
ocupação e a risco jurídico.

---

## 3. Arquitetura

```
.claude/skills/leilao-imoveis/
├── SKILL.md                      # papel do agente, fluxo, critérios de corte
├── references/                   # marco legal, modalidades da Caixa,
│   │                             # due diligence, fontes, fórmulas e pesos
│   └── 01..05-*.md
├── scripts/
│   ├── coletar_portal.py   179 l # coleta o estoque da Caixa
│   ├── triagem.py          265 l # aplica os cortes do mandato
│   ├── viabilidade.py      359 l # CTA, margem, lance máximo
│   ├── comparaveis.py      160 l # levanta o mercado (VVR)
│   ├── historico.py         75 l # registra lotes que saem da lista
│   ├── planilha.py         344 l # monta o .xlsx com fórmulas
│   ├── conferir_planilha.py 72 l # valida as fórmulas do .xlsx
│   └── varredura.sh         83 l # ciclo completo, para cron no desktop
└── templates/                    # ficha de oportunidade, schema do pipeline
```

Dados e saídas, na raiz do repositório: `perfil-investidor.md` (mandato),
`pipeline.csv` (estado corrente da triagem), `dados/` (coletas datadas,
comparáveis, histórico de saídas), `planilhas/` (entregas), `relatorios/`,
`docs/` (rede, desktop, rotina).

### Fluxo de uma rodada

```
coletar_portal.py  →  dados/caixa-lotes-AAAA-MM-DD-HHh.csv
        ↓
historico.py  (diff contra a coleta anterior)  →  dados/historico-saidas.csv
        ↓
triagem.py  (cortes do mandato)  →  pipeline.csv
        ↓
comparaveis.py  (só se o levantamento tiver 7 dias ou mais)
        ↓
planilha.py  →  planilhas/varredura-AAAA-MM-DD-HHh.xlsx
        ↓
conferir_planilha.py  (nenhuma planilha se entrega com célula em erro)
        ↓
SendUserFile + resumo de até 3 linhas + commit e push
```

Passo a passo operacional com os comandos exatos: `docs/rotina-varredura.md`.

---

## 4. Restrições do ambiente — leia antes de mexer

Estas quatro coisas custaram horas de descoberta. Ignorá-las faz o novo agente
repetir o caminho.

### 4.1 O CSV estático da Caixa está barrado

`https://venda-imoveis.caixa.gov.br/listaweb/Lista_imoveis_UF.csv` é a via
óbvia e **não funciona**: o portal roda um antirrobô (Radware/ShieldSquare) que
redireciona para `validate.perfdrive.com`. Testado 5 vezes, 5 redirecionamentos.

**A via que funciona** são os endpoints POST que o próprio formulário de busca
usa — é o que o `coletar_portal.py` faz:

| Endpoint | Método | Para quê |
|---|---|---|
| `/sistema/busca-imovel.asp` | GET | aquece a sessão, pega o cookie ASPSESSIONID |
| `/sistema/carregaListaCidades.asp` | POST `cmb_estado=UF` | códigos das cidades |
| `/sistema/carregaPesquisaImoveis.asp` | POST `hdn_estado`, `hdn_cidade` | códigos dos lotes |
| `/sistema/detalhe-imovel.asp` | **POST** `hdnImovel`, `hdnOrigem` | a ficha completa |

Dois detalhes que quebram silenciosamente:

- **Cookie de sessão é obrigatório.** Sem ele, 302 para o validador.
- **A ficha só vem por POST.** O mesmo `detalhe-imovel.asp` por GET é barrado.

Ganho colateral: a ficha por POST é **mais rica** que o CSV — traz matrícula,
comarca, ofício, inscrição imobiliária, formas de pagamento aceitas e as regras
de condomínio e tributos.

Códigos de cidade em uso: `8761` Palhoça, `8873` São José, `8621` Florianópolis.

### 4.2 A política de rede do ambiente bloqueia por domínio

Sessões na nuvem alcançam só os domínios liberados. Hoje funcionam
`caixa.gov.br` e `imoveis-sc.com.br`. **Não** funcionam: `zapimoveis.com.br` e
`vivareal.com.br` (403 de Cloudflare mesmo com User-Agent de navegador),
`chavesnamao`, `mgfimoveis`, `buskaza` (bloqueio no gateway), `viacep.com.br`
e `api.telegram.org`.

Como editar a lista: `docs/liberar-rede.md`. **A alteração só vale em sessão
nova** — a sessão aberta mantém a política com que nasceu.

### 4.3 O LibreOffice não carrega nem um arquivo trivial

O recálculo canônico de `.xlsx` seria `soffice --convert-to`. Neste contêiner
ele falha com `Error: source file could not be loaded` até num arquivo de duas
células — testado para isolar, o defeito é do ambiente, não do arquivo.

Substituto: `conferir_planilha.py` lê as fórmulas **como estão gravadas dentro
do .xlsx**, resolve as referências entre células e avalia cada uma. Confere
contra a saída do `viabilidade.py`. Não substitui abrir no Excel, e isso deve
ser dito à usuária sempre que a verificação for relatada.

### 4.4 O contêiner é efêmero e a fila de disparos falha

O que não for commitado desaparece. `openpyxl` costuma precisar de reinstalação
(`pip install openpyxl`) a cada contêiner novo.

Em 20/09 **três disparos da rotina acumularam na fila** e chegaram juntos. O
portal só expõe o estado corrente, então não há como reconstituir as janelas
perdidas: atendeu-se com uma varredura só, e isso foi relatado à usuária como
falha de entrega, não escondido. Se voltar a ocorrer, a alternativa é a rotina
abrir sessão nova a cada disparo em vez de acordar a sessão persistente — mais
confiável, ao custo de a planilha chegar por notificação.

---

## 5. Defeitos já encontrados e corrigidos

**Não reintroduza.** Todos eram silenciosos: produziam número errado sem erro.

| Defeito | Efeito | Correção |
|---|---|---|
| `"45,61m2"` lido como **45,612** — o dígito da unidade sobrevivia ao filtro de caracteres | contaminava toda área privativa, e por consequência VVR e custo de reforma | cortar a unidade (`m2`/`m²`) antes de limpar o número |
| Página lida como latin-1 quando é UTF-8 | o soft hyphen do mojibake não é `\w`, então todo rótulo com acento (`mínimo`, `condomínio`) falhava no regex | decodificar UTF-8, com latin-1 só de reserva |
| Situação de ocupação não chegava ao `triagem.py`, que a lê do campo de descrição | todo lote saía `DESCONHECIDO` e o peso de posse no score ficava errado | anexar a situação à descrição na coleta |
| Modalidade vazia em Venda Online e Venda Direta | essas páginas não têm bloco de título de certame; o `triagem.py` dava nota neutra de segurança jurídica (5/10 em vez de 9) justamente nas duas modalidades que o mandato prefere | detectar pelos endpoints (`/venda-online/`, "Fazer uma proposta") |

**Peculiaridade da fonte:** a situação de ocupação vem dentro de um **comentário
HTML** — não aparece na tela do portal, mas está no código-fonte. É informação
declarada pela Caixa e é extraída dali.

---

## 6. O que já se sabe da praça-alvo

### 6.1 Referência de mercado — Bela Vista, Palhoça (23/09/2026)

Levantada de anúncios ativos em `imoveis-sc.com.br`. Anúncio é preço pedido,
não preço fechado — daí o deságio de 0,88.

| Métrica | Valor | Base |
|---|---|---|
| Mediana apto 2 dorm. | R$ 275.000 | n=26 |
| Mediana casa | R$ 479.000 | n=53 |
| Apto 3 dorm. | **nenhum anúncio no bairro** | n=0 |
| **R$/m² da banda 42–49 m²** | **R$ 5.913** | n=13 — é esta que entra no VVR |
| Condomínio mediano | R$ 399/mês | n=20 |

**Fórmula do VVR:** `área privativa × R$ 5.913 × 0,88`.

Por que a banda e não a mediana crua: a mediana de R$ 275.000 corresponde a área
mediana de 49 m², e o estoque da Caixa no bairro tem 43,80 a 45,61 m². Usar a
mediana crua superestima o VVR.

Série histórica do R$/m²: 16/09 → R$ 5.920 (n=14); 23/09 → R$ 5.913 (n=13),
−0,1%. Uma semana não é tendência; a série existe para que uma queda de VVR não
seja confundida com movimento no portal.

**Leitura:** Bela Vista é mercado de 2 dormitórios. 3 dormitórios não tem
liquidez comprovada ali e não serve à tese de flip.

### 6.2 Os três lotes da praça-alvo, e por que nenhum fecha

Todos apartamento de 2 dormitórios com 1 vaga, **todos ocupados**, **todos
Leilão SFI**, todos com matrícula individualizada. Preço = piso do 2º leilão.

| Imóvel | Área priv. | Avaliação | Lance | VVR | CTA | Margem |
|---|---|---|---|---|---|---|
| 878770360836-7 | 45,61 m² | R$ 240.000 | R$ 144.000 | R$ 237.329 | R$ 219.842 | **+1,48%** |
| 878770561220-5 | 43,80 m² | R$ 252.000 | R$ 151.200 | R$ 227.911 | R$ 226.708 | **−5,50%** |
| 878771588251-5 | 43,80 m² | R$ 258.000 | R$ 168.933 | R$ 227.911 | R$ 246.073 | **−12,94%** |

Mínimo exigido: 25%. **O obstáculo decisivo não é a margem, é o caixa:** nenhum
dos 7 lotes de Palhoça aceita financiamento, e no melhor cenário o desembolso do
melhor lote é R$ 183 mil contra R$ 100 mil de capital — faltam R$ 83 mil.

Sensibilidade do melhor lote: otimista 21,9%; otimista com venda a preço de
anúncio 38,5%; base 1,48%; pessimista −18,7%. **O negócio existe; o capital não
alcança.**

### 6.3 A avaliação da Caixa não resiste a conferência

Dois lotes no **mesmo endereço** (Av. Paulo Roberto Vidal, 2050), mesma metragem
(50,87 m² totais / 43,80 m² privativos), mesmo CEP e inscrição imobiliária
diferindo só no dígito do bloco foram avaliados em **R$ 258.000 e R$ 223.000** —
15,7% de diferença. E a Caixa rotulou um como *Bela Vista* e o outro como
*Lot. Pq. Vale Verde*. Consequência prática: o rótulo de bairro do portal **não
é filtro confiável** de praça-alvo.

### 6.4 O que a modalidade determina (n=18)

| Modalidade | Lotes | Teto de condomínio | Permite financiamento |
|---|---|---|---|
| Leilão SFI | 15 | **0** | 0 |
| Licitação Aberta | 1 | 1 | 0 |
| Venda Online | 2 | 2 | 1 |

O **teto de condomínio acompanha a modalidade**: nenhum SFI tem; todos os lotes
fora do SFI limitam a 10% da avaliação, com a Caixa pagando o excedente. Num
lote de R$ 240 mil o teto é R$ 24 mil, acima da premissa de R$ 12 mil — **não
melhora o cenário base, elimina a cauda**.

O **financiamento não acompanha a modalidade**: dos dois lotes de Venda Online,
um permite SBPE e o outro é "exclusivamente à vista". Confere-se lote a lote.

### 6.5 Como os lotes saem da lista (n=5, todas no 2º anel)

| Constatação | n | Conclusão |
|---|---|---|
| Saiu só após esgotar **as duas** datas de certame | 5 de 5 | nenhum saiu entre o 1º e o 2º leilão |
| Piso na saída, sobre a avaliação | mediana 60,0% | é o piso do 2º leilão |
| Atraso do portal entre certame e baixa | 1 dia, 2 vezes | lote na lista no dia seguinte não é deserto |

Se algum tivesse sido arrematado no 1º leilão, teria saído antes da segunda
data. Nenhum saiu: **nesta praça o 1º leilão não fecha**, e o preço que
interessa é o do 2º. Isso sustenta o critério de tomar o piso do 2º leilão como
preço de entrada na triagem.

**Limite:** o portal não declara a causa da saída. Arremate, suspensão e
retirada são indistinguíveis daqui, e o registro nunca supõe qual foi. Cinco
casos não são estatística — **um único lote que saia entre as duas datas derruba
a conclusão**.

---

## 7. A rotina automática

Roda às **07h e 19h**, todos os dias, fuso de Brasília (cron `0 10,22 * * *` em
UTC). Entrega o `.xlsx` na conversa e comita na branch.

O resumo que acompanha tem **no máximo três linhas** e fala só do que **mudou**:
lote novo, preço que caiu, lote que saiu, certame a menos de 7 dias. **Se nada
mudou, é uma linha dizendo isso, e a planilha vai do mesmo jeito.** Movimento
inventado para justificar a rodada é pior que rodada silenciosa — e na prática a
maioria dos dias não tem movimento algum.

### A planilha

Seis abas: Leia-me, Premissas, Aprovados na triagem, Todos os lotes,
Comparáveis, Saíram da lista.

O desenho que importa: **as contas são fórmulas, não números cravados.** A aba
Premissas concentra os inputs (amarelo = a usuária edita) e as demais abas
referenciam aquelas células. Se a administradora informar que o condomínio
atrasado é R$ 4 mil e não R$ 12 mil, ela altera **uma célula** e margem, CTA,
lance máximo e veredicto dos três lotes se refazem. O lance também é editável,
para simular o certame.

Premissas atuais: comissão 5%, ITBI 3%, registro 1,2%, IPTU atrasado R$ 3.000,
condomínio atrasado R$ 12.000, consumo R$ 800, desocupação R$ 15.000, reforma
R$ 550/m², carrego R$ 559/mês, ciclo 12 meses, R$/m² 5.913, capital R$ 100.000,
entrada 100%.

---

## 8. Decisões em aberto

### 8.1 FGTS — é o que destrava ou enterra a praça-alvo

Está `A DEFINIR` no perfil e virou a variável decisiva: os três lotes de Bela
Vista **aceitam FGTS**. Se houver saldo, ele soma ao capital e refaz a conta
inteira. Se não houver, Bela Vista está fora de alcance neste ciclo e a varredura
passa a ser monitoramento.

Se houver saldo, conferir antes de qualquer lance: enquadramento (imóvel
residencial urbano, não ser proprietária de outro imóvel na região, três anos de
FGTS, teto do SFH) e, sobretudo, se o **prazo de liberação** cabe no prazo de
pagamento do edital — leilão costuma ter prazo curto demais para isso.

### 8.2 Tolerâncias

Ocupação e risco jurídico seguem `A DEFINIR`. A triagem roda com o padrão da
skill, não com o critério dela.

### 8.3 Bot de Telegram — a tarefa que provavelmente motivou este repasse

A usuária cogitou criar um bot. Foram apresentadas duas opções e **ela ainda não
escolheu**. A bifurcação muda custo, trabalho e onde a coisa roda:

**Opção A — o bot entrega a varredura.** Às 07h e 19h a planilha e o resumo
chegam no Telegram. Não usa IA nenhuma: é o script existente chamando a API do
Telegram no fim. Custo zero, sem servidor, ~20 linhas no `planilha.py` ou num
passo novo da rotina. **É a recomendada para começar.**

**Opção B — o bot conversa.** Ela pergunta "quanto posso dar de lance se o
condomínio for 4 mil?" e ele responde. Exige (i) chave da API da Anthropic, que
é produto separado e cobrado por uso — não é a assinatura do Claude dela; e
(ii) uma máquina ligada o tempo todo para escutar as mensagens, porque o
contêiner da nuvem é reciclado. O desktop dela serve (`docs/rodar-no-desktop.md`).

**Obstáculos e cuidados, para qualquer das duas:**

- `api.telegram.org` **está bloqueado** pela política de rede (403 no gateway).
  Precisa entrar na lista de domínios liberados antes de qualquer código, e a
  mudança só vale em sessão nova.
- O **token do bot é uma senha**: quem o tiver controla o bot. Não deve ser
  colado em conversa nem commitado. Lugar certo: variável de ambiente / secrets
  do ambiente. O código lê de lá.
- Na Opção B, autenticar por `chat_id` para que só ela fale com o bot. Um bot de
  Telegram aberto responde a qualquer pessoa que o encontre.
- Perguntar a ela se quer **as duas rodadas** ou **só quando houver movimento**.

---

## 9. Convenções de trabalho — o que a usuária espera

Estas não são preferências de estilo: são o contrato de confiança do projeto.

- **Nunca afirmar o que não se verificou.** Todo relatório encerra com o que
  **não** foi conferido. Até hoje: nenhuma matrícula foi lida, nenhum edital foi
  lido integralmente, nenhum débito foi confirmado, nenhuma vistoria foi feita,
  quem ocupa cada imóvel é desconhecido, os comparáveis são anúncios e não
  transações.
- **Distinguir estimativa de apuração.** "Estimativa" para as faixas de custo,
  "apurado" para o que foi medido nos comparáveis. É o que separa, num laudo, o
  que ela verificou do que presumiu.
- **Relatar impossibilidade com a causa e o substituto.** "Não foi possível"
  ≠ "não foi feito". Foi assim que se relatou o LibreOffice quebrado.
- **Corrigir em voz alta.** Quando uma leitura anterior se mostrou errada — como
  a de que Venda Online garantiria financiamento — a correção vem explícita, não
  por omissão.
- **Não inventar movimento.** Dia sem mudança é uma linha dizendo isso.
- Ela é contadora e perita: **pediu escrita em português culto formal**, e
  observações pontuais de redação aplicáveis a laudo e parecer são bem-vindas.

---

## 10. Primeiros passos sugeridos para quem assume

1. Ler `perfil-investidor.md` inteiro. É o mandato, e nada se decide sem ele.
2. Ler `docs/rotina-varredura.md` — os oito passos com os comandos exatos.
3. Rodar uma varredura manual e conferir que sai 15 a 18 lotes, 3 aprovados, e
   que o `conferir_planilha.py` acusa 64 células e 0 erro.
4. **Perguntar a ela sobre o FGTS.** É a pergunta de maior valor em aberto.
5. Se o pedido for o bot: confirmar A ou B, liberar `api.telegram.org`, e pedir
   token e `chat_id` — o token por secrets, nunca por conversa.
6. Não mexer no `viabilidade.py` sem rodar `--exemplo` antes e depois. As
   fórmulas da planilha são conferidas contra a saída dele.

---

## Aviso

Material de apoio à decisão de investimento. Não é parecer jurídico nem
avaliação imobiliária. Antes de arrematar: edital integral, matrícula
atualizada, débito de condomínio por escrito e com data, e advogado.
