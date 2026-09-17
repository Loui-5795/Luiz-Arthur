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

## Os sete passos

1. **Ler `perfil-investidor.md`.** Praça-alvo, cortes, tolerâncias e capital saem
   de lá — nunca de memória. Parâmetro em `A DEFINIR` roda com o padrão da skill
   e é registrado como pendência no resumo.

2. **Coletar o estoque da Caixa.**
   ```bash
   python3 .claude/skills/leilao-imoveis/scripts/coletar_portal.py SC \
     8761:PALHOCA dados/caixa-palhoca-AAAA-MM-DD.csv
   python3 .claude/skills/leilao-imoveis/scripts/coletar_portal.py SC \
     8873:SAO_JOSE 8621:FLORIANOPOLIS dados/caixa-anel2-AAAA-MM-DD.csv
   ```
   O download estático por UF continua barrado pelo antirrobô do portal; a coleta
   vai pelos endpoints POST do formulário de busca.

3. **Triar com os cortes do mandato.**
   ```bash
   python3 .claude/skills/leilao-imoveis/scripts/triagem.py dados/lotes.csv \
     --uf SC --cidade PALHOCA --desconto-min 25 \
     --bairros "BELA VISTA" "PEDRA BRANCA" "PASSA VINTE" "ARIRIU" \
               "JARDIM ELDORADO" "PONTE DO IMARUIM" "CAMINHO NOVO" \
     --pipeline pipeline.csv
   ```

4. **Precificar os aprovados** com `scripts/viabilidade.py`, usando o VVR do
   perfil (`área privativa × R$/m² da banda × 0,88`).

5. **Atualizar os comparáveis de mercado** se o levantamento tiver mais de
   **7 dias**. Menos que isso, reaproveita — anúncio não muda de manhã para a
   noite, e refazer a cada 12 horas só gasta requisição.

6. **Gerar a planilha.**
   ```bash
   python3 .claude/skills/leilao-imoveis/scripts/planilha.py \
     --lotes dados/caixa-lotes-AAAA-MM-DD.csv \
     --comparaveis dados/comparaveis-bela-vista-AAAA-MM-DD.csv \
     --pipeline pipeline.csv --saida planilhas/varredura-AAAA-MM-DD-HHh.xlsx
   ```

7. **Entregar:** enviar o `.xlsx` na conversa, escrever um resumo curto do que
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
