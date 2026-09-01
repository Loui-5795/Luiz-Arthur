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
| Acesso pelo celular | Sim | Não |

O melhor arranjo é híbrido: **desktop coleta e analisa**, nuvem/celular
consulta e gera documentos, e o **git é a memória compartilhada** entre os dois
e com quem mais entrar no projeto.

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

## Varredura recorrente

Dentro do Claude Code, para uma sessão de trabalho:

```
/loop 6h varra os lotes novos da Caixa em MG e me avise o que passar de 75 pontos
```

Para rodar sem ninguém na frente da tela, agende no sistema operacional:

```bash
# cron, toda segunda às 7h
0 7 * * 1 cd ~/Luiz-Arthur && claude -p "varra os lotes novos da Caixa em MG, atualize o pipeline.csv e comite" >> ~/leilao.log 2>&1
```

## Trabalhando junto com o Marco Antônio

Cada um clona o repositório e trabalha na sua máquina; o `pipeline.csv` e as
fichas de oportunidade viajam pelo git. Antes de começar, `git pull`; ao
terminar, comite e suba. Se os dois mexerem no mesmo dia, o conflito no CSV se
resolve mantendo as duas linhas — cada lote é um registro independente.
