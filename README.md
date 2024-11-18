# Legacy to Cloud Pipeline

Este projeto implementa uma pipeline completa para migrar dados de um sistema legado para uma arquitetura moderna baseada em AWS. A estrutura segue o padrão de camadas de dados (RAW, BRONZE, SILVER, GOLD) e utiliza diversos serviços AWS para armazenamento, transformação e análise.

---

## 🎯 Objetivo

Migrar e modernizar a infraestrutura de dados de um sistema legado, permitindo:
- Maior escalabilidade e eficiência.
- Estruturação de dados para análises avançadas.
- Automação de processos de ETL.

---

## 🗂️ Estrutura do Projeto

Abaixo está a organização das pastas e arquivos do projeto:

- **`docs/`**: Documentação adicional e detalhada sobre o projeto.
- **`resources/`**: Arquivos de suporte, como configurações e templates.
- **`s3/`**:
  - **`raw/`**: Dados brutos extraídos do sistema legado.
  - **`bronze/`**: Dados estruturados e limpos.
  - **`silver/`**: Dados enriquecidos e prontos para análise.
  - **`gold/`**: Dados finais otimizados para consumo analítico e dashboards.
- **`scripts/`**:
  - `01_create_db.py`: Script para criar o banco de dados legado.
  - `02_create_and_populate_tb.py`: População de tabelas no banco legado.
  - `03_export_to_raw.py`: Exportação de dados para a camada RAW no S3.
  - `04_raw_to_bronze.py`: Transformação de dados da camada RAW para BRONZE.
  - `05_bronze_to_silver.py`: Processamento de dados da camada BRONZE para SILVER.
  - `06_silver_to_gold.py`: Enriquecimento e transformação de dados da camada SILVER para GOLD.
  - `07_sales_months_analysis.py`: Análise de vendas mensais para dashboards.
  - `config.py`: Arquivo de configuração para conexões e variáveis globais.
  - `sales_vs_month.sql`: Query SQL para análise de vendas por mês.
- **`.gitignore`**: Configuração para ignorar arquivos e pastas irrelevantes no versionamento.

---

## 🚀 Como Configurar e Executar

1. **Clone este repositório**:
   ```bash
   git clone https://github.com/seu-usuario/legacy-to-cloud-pipeline.git
   cd legacy-to-cloud-pipeline

2. **Execute os scripts na ordem**:

- Crie e popule o banco legado:
    ```
    python scripts/01_create_db.py
    python scripts/02_create_and_populate_tb.py
    ```

- Exporte os dados e processe as camadas:
    ```
    python scripts/03_export_to_raw.py
    python scripts/04_raw_to_bronze.py
    python scripts/05_bronze_to_silver.py
    python scripts/06_silver_to_gold.py
    ```
- Geração de relatórios de vendas:
    ```
    python scripts/07_sales_months_analysis.py
    ```

## 📊 Benefícios do Projeto

- **Modernização de Infraestrutura**
Transição de sistemas legados para serviços escaláveis na nuvem, aumentando a eficiência operacional.

- **Automação**
Pipelines de dados automatizados que eliminam tarefas manuais, economizando tempo e reduzindo erros.

- **Escalabilidade e Flexibilidade**
A arquitetura suporta altos volumes de dados e análises avançadas, além de estar pronta para integrações futuras, como modelos preditivos e análises em tempo real.

## 📋 Licença

Este projeto está licenciado sob os termos da MIT License.