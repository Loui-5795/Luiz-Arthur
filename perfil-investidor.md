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
| Capital à vista | `A DEFINIR` |
| Ticket máximo por lote | `A DEFINIR` |
| Aceita financiamento Caixa | `A DEFINIR` |
| Aceita usar FGTS | `A DEFINIR` |

## Tese de saída

| | |
|---|---|
| Tese principal | `A DEFINIR` — revenda (flip) / renda (locação) / uso próprio |
| Ciclo aceitável | revenda: 6–12 meses |
| Margem líquida mínima | 25% sobre o CTA (padrão; revisar com a tese) |
| Cap rate mínimo | 7% a.a. (se tese de renda) |

## Tolerâncias

| | |
|---|---|
| Ocupação | `A DEFINIR` — só desocupado / aceita ex-devedor / aceita qualquer |
| Risco jurídico | `A DEFINIR` — só venda direta e licitação / aceita 2º Leilão SFI / aceita judicial |
| Tipologia | apartamento e casa residencial; terreno só com acesso e matrícula limpa |

## Cortes automáticos

Aplicados pelo `scripts/triagem.py` em toda varredura:

- desconto anunciado mínimo: **25%**
- fora da praça-alvo (núcleo + 1º anel): descarta
- acima do ticket máximo: descarta
- sem matrícula individualizada: descarta

## Referência de mercado — Bela Vista, Palhoça

Preencher e manter atualizado; é a base do VVR e, sem ele, nenhum score é real.

| Tipologia | Mediana de anúncio | Data | Nº de comparáveis | Fonte |
|---|---|---|---|---|
| Apto 2 dorm. | `A LEVANTAR` | | | |
| Apto 3 dorm. | `A LEVANTAR` | | | |
| Casa | `A LEVANTAR` | | | |
| Aluguel apto 2 dorm. | `A LEVANTAR` | | | |

Levantamento inicial (setembro/2026): a faixa praticada em Palhoça como um todo
aparece entre R$ 175 mil e R$ 750 mil para apartamentos, com Bela Vista
posicionado como bairro em expansão e de entrada mais acessível. Faixa larga
demais para servir de VVR — a primeira tarefa da primeira varredura é fechar
esses números por tipologia, com no mínimo 5 comparáveis cada.
