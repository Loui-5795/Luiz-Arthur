#!/usr/bin/env bash
# Varredura automatizada de imoveis em leilao.
#
#   ./varredura.sh              roda o ciclo uma vez
#   ./varredura.sh --agendar    instala no cron (segunda, 07h) e sai
#   ./varredura.sh --remover    remove o agendamento
#
# O ciclo: atualiza o repositorio, chama o agente com o mandato do
# perfil-investidor.md, e comita o que mudou. O julgamento e do agente; este
# script so garante que ele rode sempre igual, sem ninguem na frente da tela.

set -euo pipefail

CRON_PADRAO="0 7 * * 1"          # toda segunda-feira, 07h
MARCADOR="# leilao-imoveis-varredura"

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(git -C "$AQUI" rev-parse --show-toplevel)"
LOGDIR="$REPO/logs"
LOCK="$REPO/.varredura.lock"

case "${1:-}" in
  --agendar)
    linha="$CRON_PADRAO cd $REPO && $AQUI/varredura.sh >> $LOGDIR/cron.log 2>&1 $MARCADOR"
    atual="$(crontab -l 2>/dev/null | grep -v "$MARCADOR" || true)"
    printf '%s\n%s\n' "$atual" "$linha" | sed '/^$/d' | crontab -
    echo "Agendado: $CRON_PADRAO"
    crontab -l | grep "$MARCADOR"
    exit 0
    ;;
  --remover)
    crontab -l 2>/dev/null | grep -v "$MARCADOR" | crontab - || true
    echo "Agendamento removido."
    exit 0
    ;;
esac

command -v claude >/dev/null || { echo "claude CLI nao encontrado no PATH."; exit 1; }
mkdir -p "$LOGDIR"

# Trava: uma varredura por vez. Rodada sobreposta gera conflito no pipeline.
if ! mkdir "$LOCK" 2>/dev/null; then
  echo "Ja existe uma varredura em andamento ($LOCK). Saindo."
  exit 0
fi
trap 'rmdir "$LOCK" 2>/dev/null || true' EXIT

LOG="$LOGDIR/varredura-$(date +%F).log"
exec > >(tee -a "$LOG") 2>&1
echo "=== varredura $(date '+%F %T') ==="

cd "$REPO"
git pull --rebase --autostash origin "$(git rev-parse --abbrev-ref HEAD)" || \
  echo "aviso: pull falhou, seguindo com a copia local"

claude -p --permission-mode auto "$(cat <<'PROMPT'
Rode a varredura semanal de imoveis em leilao, seguindo a skill leilao-imoveis.

1. Leia perfil-investidor.md e use a praca-alvo, os cortes e as tolerancias de
   la. Se algum parametro estiver "A DEFINIR", use o padrao da skill e registre
   no relatorio que ele ficou pendente.
2. Varra as fontes de references/04-fontes-e-plataformas.md, comecando pela
   Caixa. Baixe a lista da UF e passe por scripts/triagem.py.
3. Compare com o pipeline.csv: interessa o que e novo, o que mudou de preco e
   o que saiu. Nao reanalise lote ja descartado, a menos que o preco tenha caido.
4. Para os lotes que passarem na triagem, faca a due diligence possivel sem
   contato humano (matricula publica, edital, debitos declarados) e rode
   scripts/viabilidade.py com comparaveis reais da microrregiao.
5. Atualize pipeline.csv, escreva relatorio-YYYY-MM-DD.md em relatorios/ com os
   lotes ranqueados, os riscos nomeados e o que NAO foi verificado, e publique
   o painel de oportunidades como Artifact, republicando sempre no mesmo link.
6. Se nada novo apareceu, diga isso em uma linha e nao invente movimento.
PROMPT
)"

if [[ -n "$(git status --porcelain)" ]]; then
  git add -A
  git commit -q -m "Varredura automatica $(date +%F)"
  git push -q origin "$(git rev-parse --abbrev-ref HEAD)" && echo "alteracoes enviadas"
else
  echo "nada mudou nesta rodada"
fi
echo "=== fim $(date '+%F %T') ==="
