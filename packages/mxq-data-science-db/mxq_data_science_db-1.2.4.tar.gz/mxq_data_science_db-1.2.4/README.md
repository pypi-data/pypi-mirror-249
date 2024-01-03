# mxq_data_science_db
Python packages para gerenciamento dos bancos de dados relacionados ao data science.

## Settings
Scripts para gerenciar secrets e ENV variables. Secrets são gerenciados via AWS secret manager em [terraform](https://github.com/maxiquimltda/terraform/tree/main/aws/data_science/secret_manager).
## DBs
Gerenciamento dos bancos de dados e data models.

### db_economia
Data models relacionados ao produto MXQ economia com reports relacionados a IPCA, cambio...

## Build
Para buildar o packages, utilize o comando `poetry build`

## Models
### db_economia

- **agregado**: dimensional table para salvar os meta dados dos agregados do IBGE, a principio não utilizado para analises
- **dados_ibge**: tabela onde será salvo os dados para analise com indicadores provenientes do IBGE.
- **cambio**: tabela nova para salvar dados de cambio.

### db_commodities
- **anp_processamento_petroleo**: tabela com dados da ANP de processamento de petroleo.
- **anp_producao_derivados**: tabela com dados da ANP de produção de derivados.
- **anp_producao_petroleo_gn**: tabela com dados da ANP de produção de petroleo e GN.
- **anp_venda_derivados**: tabela com dados da ANP de venda de derivados.

### db_comex
- **ncm**: Antigo arquivo em excel `matriz_maxiquim.xlsx` com NCM por material para o BR.
- **mmi_comex_br_processed**: Dados processados e filtrados para serem utilizados no MMI.