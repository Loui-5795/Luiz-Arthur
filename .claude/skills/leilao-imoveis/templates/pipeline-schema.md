# `pipeline.csv` — schema

Um registro por lote analisado, **inclusive os descartados**. É o que impede
reanalisar o mesmo lixo todo mês e o que calibra a agressividade dos lances.

```csv
id,data_analise,comitente,modalidade,uf,cidade,bairro,tipo,area_m2,matricula,
valor_avaliacao,lance_minimo,vvr,cta_no_minimo,lance_maximo,margem_projetada,
score,ocupacao,debitos_declarados,data_certame,plataforma,link_edital,
status,motivo_descarte,resultado,valor_arrematado,arrematante
```

| Coluna | Domínio |
|---|---|
| `modalidade` | `1LEILAO_SFI` `2LEILAO_SFI` `LICITACAO_ABERTA` `VENDA_ONLINE` `VENDA_DIRETA` `JUDICIAL` `EXTRAJUDICIAL_OUTRO` |
| `ocupacao` | `DESOCUPADO` `EX_DEVEDOR` `LOCATARIO` `TERCEIRO` `DESCONHECIDO` |
| `status` | `TRIAGEM` `DUE_DILIGENCE` `HABILITADO` `LANCE_DADO` `ARREMATADO` `PERDIDO` `DESCARTADO` |
| `motivo_descarte` | texto curto e padronizado (ex.: `desconto_real_baixo`, `ocupacao_terceiro`, `matricula_suja`, `prazo_insuficiente`) |
| `resultado` | preenchido após o certame |
| `valor_arrematado` | valor vencedor, mesmo quando o lote foi perdido — é o dado que calibra os próximos lances |

Convenções: valores em reais sem separador de milhar; datas em `YYYY-MM-DD`;
campo desconhecido preenchido com `NV` (não verificado), nunca vazio.
