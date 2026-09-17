# Agente de Imóveis em Leilão

Agente para prospecção, triagem e análise de oportunidades em imóveis de leilão
e de venda de bancos — Caixa (1º e 2º Leilão SFI, Licitação Aberta, Venda Online
e Venda Direta), demais agentes financeiros, e leilões judiciais.

O agente não lista leilões: ele **separa oportunidade real de armadilha** e
entrega recomendação com números, riscos nomeados e um lance máximo defensável.

## Como usar

O agente é uma *skill* do Claude Code. Basta abrir este repositório com o Claude
Code e pedir, em linguagem natural:

```
Garimpe apartamentos da Caixa em Belo Horizonte até R$ 250 mil,
tese de revenda em 12 meses.
```

```
Analise este edital e me diga o lance máximo: <link>
```

```
Rode a viabilidade deste lote: lance 180k, avaliação 320k, 62 m²,
condomínio atrasado 11k, ocupado pelo ex-devedor.
```

A skill é acionada automaticamente por termos como *leilão*, *imóvel retomado*,
*praça*, *arrematação*, *edital*, *alienação fiduciária*, *imissão na posse*.

### Calculadora de viabilidade, sozinha

```bash
python3 .claude/skills/leilao-imoveis/scripts/viabilidade.py --exemplo
python3 .claude/skills/leilao-imoveis/scripts/viabilidade.py --json lote.json
python3 .claude/skills/leilao-imoveis/scripts/viabilidade.py --json carteira.json --formato json
```

Calcula o Custo Total de Aquisição, a margem líquida, o retorno anualizado, o
desconto real e o **lance máximo** que ainda entrega a margem-alvo. Aceita um
lote ou uma lista, e ranqueia. Sem dependências além do Python 3.

## Estrutura

```
.claude/skills/leilao-imoveis/
├── SKILL.md                              # o agente: papel, fluxo, critérios de corte
├── references/
│   ├── 01-regulamento-leiloes.md         # marco legal, débitos, posse, nulidades
│   ├── 02-caixa-modalidades.md           # as 5 modalidades da Caixa e como garimpar
│   ├── 03-due-diligence-checklist.md     # checklist item a item
│   ├── 04-fontes-e-plataformas.md        # onde buscar, por banco e por tribunal
│   └── 05-analise-financeira.md          # fórmulas, faixas de custo, pesos do score
├── scripts/
│   ├── coletar_portal.py                 # coleta a lista da Caixa pelos endpoints do portal
│   ├── triagem.py                        # aplica os cortes do mandato à lista
│   └── viabilidade.py                    # calculadora de CTA e lance máximo
└── templates/
    ├── ficha-oportunidade.md             # ficha por lote
    └── pipeline-schema.md                # schema do pipeline.csv
```

## Rotina automática

A varredura roda sozinha **às 07h e às 19h**, todos os dias: coleta o estoque da
Caixa, tria pelo mandato, precifica, gera a planilha `.xlsx` e entrega na
conversa. Passo a passo e critérios em [`docs/rotina-varredura.md`](docs/rotina-varredura.md).

## Os dois princípios

1. **Desconto não é lucro.** O número que decide é o Custo Total de Aquisição
   contra o Valor de Venda Rápida — não o percentual anunciado sobre uma
   avaliação que ninguém auditou.
2. **O edital manda.** Regra geral serve para triagem; decisão de lance se toma
   lendo o edital daquele lote e a matrícula daquele imóvel.

## Aviso

Material de apoio à decisão de investimento. Não é parecer jurídico nem
avaliação imobiliária. Legislação, jurisprudência e regras de cada comitente
mudam — as referências foram compiladas em agosto/2026 e devem ser reconferidas.
Antes de arrematar, leia o edital integral, obtenha a matrícula atualizada e
consulte advogado.
