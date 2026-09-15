# Rodar este projeto no desktop

O agente funciona igual na nuvem e no desktop — o que muda é o que ele
**consegue alcançar** e o que **fica guardado**. Para operação de verdade
(varredura periódica de portais), o desktop é o lugar certo.

## O que muda

| | Nuvem (claude.ai/code) | Desktop |
|---|---|---|
| Acesso aos portais (Caixa, bancos, leiloeiras) | Bloqueado pela política de rede do ambiente (403 no gateway) | **Direto** |
| Navegador para o portal da Caixa | Depende de liberar o domínio | Instalável, sem restrição |
| `pipeline.csv` e fichas | Container é reciclado — some se não commitar | **Fica no disco** |
| Agendamento (varredura semanal) | Routines na nuvem | cron / Agendador do Windows |
| Acesso pelo celular | Sim | A sessão roda na máquina; o resultado chega por git e pelo painel |

O melhor arranjo é híbrido: **o desktop coleta**, os demais dispositivos
consultam, e o **git é a memória compartilhada** entre eles e com quem mais
entrar no projeto. Rodar no desktop não tira o projeto do celular — só a sessão
do CLI é que fica presa à máquina; o pipeline e o painel continuam acessíveis de
qualquer lugar.

## Instalação

**1. Instalar o Claude Code**

```bash
# macOS, Linux, WSL
curl -fsSL https://claude.ai/install.sh | bash

# macOS via Homebrew
brew install --cask claude-code
```

```powershell
# Windows PowerShell
irm https://claude.ai/install.ps1 | iex
```

No Windows nativo, instale também o [Git for Windows](https://git-scm.com/downloads/win)
para o Claude ter um shell decente. Confira com:

```bash
claude --version
```

**2. Entrar na conta**

```bash
claude
```

Na primeira execução ele abre o navegador para login. É a mesma assinatura —
não precisa de chave de API.

**3. Clonar o projeto**

```bash
git clone https://github.com/Loui-5795/Luiz-Arthur.git
cd Luiz-Arthur
git checkout claude/imoveis-leilao-agent-olmf6r
claude
```

Pronto. A skill `leilao-imoveis` é carregada sozinha ao abrir a pasta —
digite `/` para vê-la na lista.

**4. Opcional: navegador para o portal da Caixa**

O portal monta a busca com formulário e sessão; se requisição simples não
bastar, instale um navegador controlável (requer Node.js):

```bash
npx playwright install chromium
```

Só faça isso se o agente disser que precisa.

## Primeiro uso

```
Defina meu perfil de investidor: praça-alvo Belo Horizonte e região,
capital de R$ 250 mil à vista, tese de revenda em 12 meses.
```

```
Baixe a lista completa de imóveis da Caixa em MG e faça a triagem
inicial contra o meu perfil.
```

```
Rode a viabilidade do lote 8444712345678 e me dê o lance máximo.
```

## Guardar o trabalho

O que der resultado, comite — é isso que sobrevive à máquina e ao tempo:

```
commite o pipeline atualizado e suba
```

O `pipeline.csv` **deve** ir para o repositório: é o histórico de tudo que já
foi analisado, inclusive os descartes e os valores vencedores dos lotes
perdidos. É ele que impede reanalisar o mesmo lixo todo mês e o que calibra a
agressividade dos próximos lances.

## Começando agora — Windows, praça Palhoça / Bela Vista, tese de revenda

Abra o **PowerShell** e siga na ordem.

```powershell
# 1. instalar o Claude Code
irm https://claude.ai/install.ps1 | iex
claude --version
```

Instale também o [Git for Windows](https://git-scm.com/downloads/win), se ainda
não tiver — sem ele o Claude cai no PowerShell como shell e perde ferramenta.

```powershell
# 2. clonar e entrar
git clone https://github.com/Loui-5795/Luiz-Arthur.git
cd Luiz-Arthur
git checkout claude/imoveis-leilao-agent-olmf6r

# 3. primeira sessão: fechar o capital e levantar o mercado do bairro
claude
```

Dentro da sessão, na primeira vez:

```
Complete o perfil-investidor.md com meu capital disponível e ticket máximo,
depois levante a referência de mercado de Bela Vista, Palhoça: mediana de
anúncio por tipologia, mínimo de 5 comparáveis cada, e preencha a tabela.
```

```
Rode a varredura completa da minha praça-alvo e me traga os lotes ranqueados
com lance máximo.
```

O levantamento de mercado não é burocracia: sem a mediana do bairro não existe
VVR, e sem VVR nenhuma margem é real — é o passo que separa "imóvel barato" de
"desconto de verdade". Numa tese de flip, é ele que define se o negócio existe.

### 4. Deixar rodando sozinho

No PowerShell **como administrador**, uma vez só:

```powershell
$repo = (Get-Location).Path     # execute de dentro da pasta Luiz-Arthur

$cmd = 'claude -p --permission-mode auto "Rode a varredura semanal de imoveis ' +
       'em leilao seguindo a skill leilao-imoveis e o perfil-investidor.md. ' +
       'Atualize o pipeline.csv, escreva o relatorio em relatorios/, republique ' +
       'o painel de oportunidades e comite tudo."; ' +
       'if ((git status --porcelain).Length -gt 0) { git add -A; ' +
       'git commit -q -m ("Varredura automatica " + (Get-Date -Format yyyy-MM-dd)); ' +
       'git push -q }'

$acao = New-ScheduledTaskAction -Execute "powershell.exe" `
  -Argument "-NoProfile -ExecutionPolicy Bypass -Command `"$cmd`"" `
  -WorkingDirectory $repo
$gatilho = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 7am
$cfg = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun

Register-ScheduledTask -TaskName "LeilaoImoveis-Varredura" -Action $acao `
  -Trigger $gatilho -Settings $cfg -Force
```

`-StartWhenAvailable` recupera a rodada se o computador estava desligado às 7h;
`-WakeToRun` acorda a máquina se ela estiver suspensa.

Conferir, rodar na hora ou desfazer:

```powershell
Get-ScheduledTask -TaskName "LeilaoImoveis-Varredura"
Start-ScheduledTask -TaskName "LeilaoImoveis-Varredura"
Unregister-ScheduledTask -TaskName "LeilaoImoveis-Varredura" -Confirm:$false
```

### Alternativa: WSL

Se você usa WSL, o caminho é mais curto — `varredura.sh --agendar` faz tudo
(pull, agente, commit, push, trava contra rodadas sobrepostas e log datado):

```bash
curl -fsSL https://claude.ai/install.sh | bash
git clone https://github.com/Loui-5795/Luiz-Arthur.git
cd Luiz-Arthur && git checkout claude/imoveis-leilao-agent-olmf6r
.claude/skills/leilao-imoveis/scripts/varredura.sh --agendar
```

## Automação: rodar sozinho e chegar em todos os dispositivos

A arquitetura é esta — a máquina faz o trabalho pesado, o resultado viaja:

```
  desktop (agendado)                       qualquer dispositivo
  ------------------                       --------------------
  varre os portais                         abre o projeto na nuvem
  atualiza pipeline.csv        ──git──>    lê o pipeline atualizado
  commita e sobe                           pede análise, gera documento
  republica o painel           ──link──>   abre o painel no celular
```

O desktop é o **coletor**. Os dispositivos consomem o resultado por dois canais
que não dependem dele: o repositório e o link do painel.

### 1. O agendamento

Execução desassistida exige modo de permissão explícito — sem isso o Claude
para no primeiro pedido de confirmação e o cron fica pendurado até estourar o
tempo. Use `--permission-mode auto`, que aprova o rotineiro e ainda barra o
que foge do esperado:

```bash
# cron — toda segunda às 7h
0 7 * * 1 cd ~/Luiz-Arthur && claude -p --permission-mode auto \
  "Varra os lotes novos da Caixa na minha praça-alvo, atualize o pipeline.csv, \
   republique o painel de oportunidades e comite tudo" \
  >> ~/leilao.log 2>&1
```

No Windows, o Agendador de Tarefas com a mesma linha (programa `claude`,
argumentos idênticos, iniciar em `C:\...\Luiz-Arthur`).

`bypassPermissions` também funciona e pula toda checagem — evite: uma
automação que varre sites externos e escreve no repositório é exatamente o tipo
de coisa que você quer com freio.

### 2. Os dois canais de entrega

**Repositório.** O `git push` no fim de cada varredura é o que leva o pipeline
para todos os lugares. Do celular, você abre o projeto na nuvem e ele já vem com
a lista atualizada — pode pedir análise de um lote, rodar viabilidade, gerar
documento.

**Painel.** O agendamento republica um painel de oportunidades **no mesmo link**
a cada rodada: os lotes ranqueados, score, CTA, lance máximo e o que mudou desde
a semana passada. Abre em qualquer navegador, sem sessão, sem login — é o link
que você manda para o Marco Antônio e ele consulta de onde estiver.

### 3. A limitação real

Cron só roda com a máquina ligada e acordada. Notebook fechado às 7h da segunda
não varre nada. Duas saídas:

- Agende para um horário em que a máquina costuma estar ligada.
- Não se preocupe demais: a varredura é diferencial — compara os portais contra
  o `pipeline.csv`. Uma rodada perdida é recuperada na seguinte, sem furo no
  histórico.

Se um dia quiser automação que roda mesmo com tudo desligado, é o caminho da
nuvem — Routines na infraestrutura da Anthropic — e aí volta a depender de
liberar os domínios na política de rede do ambiente.

## Trabalhando junto com o Marco Antônio

Cada um clona o repositório e trabalha na sua máquina; o `pipeline.csv` e as
fichas de oportunidade viajam pelo git. Antes de começar, `git pull`; ao
terminar, comite e suba. Se os dois mexerem no mesmo dia, o conflito no CSV se
resolve mantendo as duas linhas — cada lote é um registro independente.
