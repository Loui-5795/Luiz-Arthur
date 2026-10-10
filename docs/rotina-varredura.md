# Rotina da varredura — o que roda às 07h e às 19h

Rotina fixa. Quem executa é o agente; este arquivo existe para que toda rodada
saia igual e para que você possa conferir o que foi feito.

## Cadência

| | |
|---|---|
| Horário | **07h00 e 19h00**, todos os dias |
| Fuso | Horário de Brasília (UTC−3) — cron em UTC: `0 10,22 * * *` |
| Entrega | Um `.xlsx` enviado **nesta conversa**, com aviso de que está pronto |
| Branch | `claude/venda-imoveis-caixa-access-22lqqc` |

## Os dez passos

1. **Ler `perfil-investidor.md`.** Praça-alvo, cortes, tolerâncias e capital saem
   de lá — nunca de memória. Parâmetro em `A DEFINIR` roda com o padrão da skill
   e é registrado como pendência no resumo.

2. **Coletar o estoque da Caixa.**
   **Uma cidade por arquivo.** O coletor é tudo-ou-nada por execução: se um lote
   não vier completo, ele não grava nada e sai com código 2. Juntar cidades numa
   só chamada faz a instabilidade de uma descartar o trabalho das outras.
   ```bash
   S=.claude/skills/leilao-imoveis/scripts
   python3 $S/coletar_portal.py SC 8761:PALHOCA        dados/caixa-palhoca-AAAA-MM-DD-HHh.csv
   python3 $S/coletar_portal.py SC 8873:SAO_JOSE       dados/caixa-saojose-AAAA-MM-DD-HHh.csv
   python3 $S/coletar_portal.py SC 8621:FLORIANOPOLIS  dados/caixa-floripa-AAAA-MM-DD-HHh.csv
   ```
   Depois concatena-se o 2º anel em `caixa-anel2-...csv` e tudo em
   `caixa-lotes-...csv`, que é o arquivo do diff e da planilha.

   O download estático por UF continua barrado pelo antirrobô do portal; a coleta
   vai pelos endpoints POST do formulário de busca.

   **Nunca aceitar coleta parcial.** Desde 04/10/2026 o coletor exige bairro,
   preço, avaliação e área privativa em cada lote, repete a página de detalhe até
   quatro vezes, **repete também a busca da cidade até quatro vezes quando ela
   volta vazia** — o portal responde 200 com zero lotes de forma intermitente — e
   **falha em voz alta** se um lote não completar ou se a busca não se recuperar. Antes dessa correção ele gravava a linha em
   branco, o lote entrava na planilha sem bairro nem preço, a triagem o
   descartava como `fora_do_bairro` e o diff lia a lista encurtada como saída.
   Código de saída 2 significa **refazer**, nunca seguir com o que veio.

3. **Conferir a coleta contra a anterior**, antes de triar.
   ```bash
   python3 .claude/skills/leilao-imoveis/scripts/conferir_coleta.py \
     --anterior dados/caixa-lotes-<rodada anterior>.csv \
     --atual dados/caixa-lotes-AAAA-MM-DD-HHh.csv
   ```
   Acusa campo que esvaziou em bloco e sai com erro. **Campo que esvazia para
   todos os lotes de uma vez é mudança na fonte, não fato do mercado** — em
   10/10/2026 a Caixa retirou a situação de ocupação de todos os dezessete
   lotes. Erro aqui significa **ir olhar a página da fonte**, nunca seguir com a
   coleta.

4. **Triar com os cortes do mandato.**
   ```bash
   python3 .claude/skills/leilao-imoveis/scripts/triagem.py dados/lotes.csv \
     --uf SC --cidade PALHOCA --desconto-min 25 \
     --bairros "BELA VISTA" "PEDRA BRANCA" "PASSA VINTE" "ARIRIU" \
               "JARDIM ELDORADO" "PONTE DO IMARUIM" "CAMINHO NOVO" \
     --pipeline pipeline.csv
   ```

5. **Registrar quem saiu da lista.**
   ```bash
   python3 .claude/skills/leilao-imoveis/scripts/historico.py \
     --anterior dados/caixa-lotes-<rodada anterior>.csv \
     --atual dados/caixa-lotes-AAAA-MM-DD-HHh.csv \
     --historico dados/historico-saidas.csv \
     --quarentena dados/ausencias-pendentes.csv --data DD/MM/AAAA
   ```
   O `triagem.py` reescreve o `pipeline.csv` a partir da lista corrente, então
   lote que sai do portal sumiria sem deixar rastro. É justamente esse o dado
   que calibra lance futuro. O portal **não declara a causa da saída** — o
   registro guarda o fato observado e nunca supõe arremate.

   **A regra das duas rodadas é obrigatória.** O `--quarentena` a aplica: a
   primeira ausência não vale saída, fica pendente; confirma-se quando o lote
   falta em duas rodadas consecutivas. Reaparecendo, sai da quarentena sem ter
   sujado o histórico. A regra nasceu de uma retratação — em 02/10/2026 um lote
   de Venda Online foi registrado como saída e reapareceu intacto na rodada
   seguinte. **Nunca rodar o `historico.py` sem o `--quarentena`**, e passar o
   mesmo arquivo ao `planilha.py`, que declara as pendências na aba de saídas.

6. **Recalcular o panorama de modalidade**, nunca atualizá-lo de memória.
   ```bash
   python3 .claude/skills/leilao-imoveis/scripts/panorama.py \
     --dados dados --saida dados/panorama-modalidade.csv
   ```
   Lê todas as coletas já gravadas, conta cada lote uma única vez e imprime a
   tabela pronta para o `perfil-investidor.md`, além de listar os lotes que
   aceitam financiamento. Existe porque a tabela feita à mão envelheceu sem
   parecer velha: registrava zero financiamentos em Leilão SFI quando o estoque
   já trazia um. **Se a tabela do perfil divergir da saída do script, o script
   está certo.**

7. **Precificar os aprovados** com `scripts/viabilidade.py`, usando o VVR do
   perfil (`área privativa × R$/m² da banda × 0,88`).

8. **Atualizar os comparáveis de mercado** se o levantamento tiver **7 dias ou
   mais**. Menos que isso, reaproveita — anúncio não muda de manhã para a noite,
   e refazer a cada 12 horas só gasta requisição.
   ```bash
   python3 .claude/skills/leilao-imoveis/scripts/comparaveis.py \
     --cidade palhoca --bairro bela-vista --banda 42-49 \
     --saida dados/comparaveis-bela-vista-AAAA-MM-DD.csv
   ```
   Depois: atualizar o R$/m² da banda e o condomínio mediano na premissa do
   `planilha.py`, acrescentar a linha à série histórica do `perfil-investidor.md`
   e **avisar no resumo** que o VVR mudou por causa do mercado, e não por
   movimento no portal — senão a usuária confunde as duas coisas.

9. **Gerar e conferir a planilha.**
   ```bash
   python3 .claude/skills/leilao-imoveis/scripts/planilha.py \
     --lotes dados/caixa-lotes-AAAA-MM-DD.csv \
     --comparaveis dados/comparaveis-bela-vista-AAAA-MM-DD.csv \
     --historico dados/historico-saidas.csv \
     --quarentena dados/ausencias-pendentes.csv \
     --pipeline pipeline.csv --saida planilhas/varredura-AAAA-MM-DD-HHh.xlsx
   python3 .claude/skills/leilao-imoveis/scripts/conferir_planilha.py \
     planilhas/varredura-AAAA-MM-DD-HHh.xlsx
   ```
   O `conferir_planilha.py` avalia as fórmulas como estão gravadas no arquivo.
   O recálculo canônico seria o LibreOffice, que neste ambiente não carrega nem
   um arquivo trivial. **Nenhuma planilha se entrega com célula em erro.**

10. **Entregar:** enviar o `.xlsx` na conversa, escrever um resumo curto do que
   **mudou** desde a rodada anterior, e comitar tudo na branch designada.

## O resumo que acompanha a planilha

Três linhas, no máximo. O que interessa é a **diferença**:

- lote novo na praça-alvo;
- preço que caiu (2º leilão costuma entrar sete dias depois do 1º);
- lote que saiu da lista (arrematado, suspenso ou adiado);
- certame a menos de 7 dias — aí o aviso vem em primeiro lugar, porque
  habilitação em plataforma de leiloeiro exige cadastro prévio.

**Se nada mudou, o resumo é uma linha dizendo isso.** A planilha vai junto de
qualquer forma. Movimento inventado para justificar a rodada é pior que rodada
silenciosa.

## Quando a rodada falha

A varredura depende de dois domínios liberados na política de rede do ambiente:
`caixa.gov.br` (o estoque) e `imoveis-sc.com.br` (os comparáveis). Se algum sair
da lista, ou se o antirrobô do portal apertar, a rodada avisa o que falhou e
entrega a planilha com o que conseguiu — nunca finge que coletou.

Lista de domínios e como editá-la: `docs/liberar-rede.md`.
