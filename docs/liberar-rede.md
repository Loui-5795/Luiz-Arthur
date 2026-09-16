# Liberar o acesso de rede do ambiente

Sessões na nuvem só alcançam os domínios que a política de rede do ambiente
permitir. Por padrão o nível é **Trusted**, que libera registries de pacote e
GitHub — e mais nada. Portais de leilão ficam de fora, e é por isso que a
varredura não roda na nuvem.

## Onde se edita

Não existe página de configurações nem URL direta: é pelo seletor de ambiente.

1. Abra **claude.ai/code**.
2. Na linha **acima da caixa de mensagem**, clique no ícone de nuvem que mostra
   o nome do ambiente atual (aqui: **agente leiloeiro**).
3. Passe o mouse sobre o ambiente na lista e clique na **engrenagem** que
   aparece à direita.
4. No campo **Network access**, troque de `Trusted` para **`Custom`**.
5. Cole a lista abaixo no campo **Allowed domains**, um domínio por linha.
6. **Marque** a caixa *"Also include default list of common package managers"*.
   Sem ela, o ambiente perde npm, PyPI e `raw.githubusercontent.com`.
7. Salve.

Os quatro níveis disponíveis: **None** (sem rede), **Trusted** (padrão),
**Full** (qualquer domínio) e **Custom** (sua lista). Prefira `Custom`:
`Full` abre a internet inteira sem necessidade.

## A lista

```
caixa.gov.br
*.caixa.gov.br
bb.com.br
*.bb.com.br
*.bradesco.com.br
*.itau.com.br
*.santander.com.br
portalzuk.com.br
*.portalzuk.com.br
megaleiloes.com.br
*.megaleiloes.com.br
sodresantoro.com.br
*.sodresantoro.com.br
frazaoleiloes.com.br
*.frazaoleiloes.com.br
biasileiloes.com.br
*.biasileiloes.com.br
leilaoimovel.com.br
*.leilaoimovel.com.br
listaleilaocaixa.com.br
*.listaleilaocaixa.com.br
zapimoveis.com.br
*.zapimoveis.com.br
vivareal.com.br
*.vivareal.com.br
imoveis-sc.com.br
*.imoveis-sc.com.br
tjsc.jus.br
*.tjsc.jus.br
palhoca.sc.gov.br
*.palhoca.sc.gov.br
```

O que cada bloco resolve:

| Bloco | Para quê |
|---|---|
| Caixa | A lista de imóveis e os editais — a fonte principal |
| Bancos | Estoque retomado de BB, Bradesco, Itaú e Santander |
| Leiloeiras | Leilões judiciais e extrajudiciais agregados |
| Portais imobiliários | **Os comparáveis de mercado** — sem eles não existe VVR, e sem VVR nenhuma margem é real |
| TJSC | Pauta de hastas públicas e consulta processual da comarca |
| Palhoça | IPTU, valor venal e regularidade da edificação |

## Depois de salvar

A configuração fica gravada no ambiente: vale para **todas as sessões futuras,
de qualquer dispositivo**, até você mudar. Mas a sessão que já está aberta
manteve a política com que nasceu — **abra uma sessão nova** para o ajuste valer.

## O que isso libera, e o que não libera

Libera **leitura de páginas públicas** nesses domínios. Não dá acesso a conta,
login ou dado bancário: a sessão não tem suas credenciais, e nenhum desses
portais entrega informação de cliente sem autenticação. O que muda é que o
agente passa a conseguir abrir a lista de imóveis e os editais sozinho, em vez
de depender de você baixar e enviar o arquivo.
