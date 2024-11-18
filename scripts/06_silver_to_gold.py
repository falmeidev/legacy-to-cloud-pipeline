import pandas as pd
import os
import glob

# Definir caminhos para as camadas Silver e Gold
SILVER_DATA_PATH = "s3/silver/sales_silver"  # Diretório da camada Silver
GOLD_DATA_PATH = "s3/gold/"  # Diretório base para a camada Gold

# Garantir que o diretório da camada Gold exista
def ensure_gold_directory_exists():
    # Verifica se o caminho definido em 'GOLD_DATA_PATH' existe
    if not os.path.exists(GOLD_DATA_PATH):
        # Cria o diretório caso ele não exista
        os.makedirs(GOLD_DATA_PATH)
        # Mensagem informando que o diretório foi criado
        print(f"Diretório criado: {GOLD_DATA_PATH}")
    else:
        # Se o diretório já existir, exibe uma mensagem informativa
        print(f"Diretório já existe: {GOLD_DATA_PATH}")

# Processar os dados da camada Silver e criar as tabelas dimensionais e fato
def process_and_move_to_gold():
    # Encontra todos os arquivos no formato Parquet armazenados na camada Silver
    silver_files = glob.glob(os.path.join(SILVER_DATA_PATH, "*.parquet"))

    # Verifica se existem arquivos na camada Silver
    if not silver_files:
        # Mensagem caso não existam dados
        print("Nenhum arquivo Parquet encontrado na camada Silver.")
        return # Finaliza a função se não houver arquivos para processar

    # Carrega todos os arquivos Parquet encontrados em um único DataFrame utilizando pandas
    sales_data = pd.concat([pd.read_parquet(file) for file in silver_files], ignore_index=True)
    print(f"Dados carregados da camada Silver. Total de linhas: {len(sales_data)}")

    # **Criação das Dimensões**
    # Dimensão 'Produto': Lista única de produtos (IDs)
    dim_product = sales_data[['product_id']].drop_duplicates().reset_index(drop=True)
    # Dimensão 'Cliente': Combina cliente com sua região, eliminando duplicatas
    dim_customer = sales_data[['customer_id', 'region']].drop_duplicates().reset_index(drop=True)
    # Dimensão 'Vendedor': Lista única de IDs de vendedores
    dim_seller = sales_data[['seller_id']].drop_duplicates().reset_index(drop=True)
    # Dimensão 'Data': Lista única de datas com atributos adicionais (ano, mês, dia)
    dim_date = sales_data[['sale_date']].drop_duplicates().reset_index(drop=True)
    dim_date['year'] = pd.to_datetime(dim_date['sale_date']).dt.year # Extração do ano
    dim_date['month'] = pd.to_datetime(dim_date['sale_date']).dt.month # Extração do mês
    dim_date['day'] = pd.to_datetime(dim_date['sale_date']).dt.day # Extração do dia

    # **Criação da Tabela Fato**
    # Contém informações transacionais das vendas (chaves de dimensão e métricas)
    fact_sales = sales_data[['sale_date', 'product_id', 'customer_id', 'seller_id', 'quantity', 'total_value']]

    # **Agregação Diária**
    # Agrupa as vendas por data e calcula métricas como total de vendas e quantidade total
    daily_sales = fact_sales.groupby('sale_date').agg(
        total_sales=('total_value', 'sum'),
        total_quantity=('quantity', 'sum')
    ).reset_index()

    # **Salvar Dimensões e Tabelas Fato na Camada Gold**
    # Cada dimensão e tabela fato é salva como um arquivo Parquet separado na camada Gold
    dim_product.to_parquet(os.path.join(GOLD_DATA_PATH, "dim_product.parquet"), index=False)
    dim_customer.to_parquet(os.path.join(GOLD_DATA_PATH, "dim_customer.parquet"), index=False)
    dim_seller.to_parquet(os.path.join(GOLD_DATA_PATH, "dim_seller.parquet"), index=False)
    dim_date.to_parquet(os.path.join(GOLD_DATA_PATH, "dim_date.parquet"), index=False)
    fact_sales.to_parquet(os.path.join(GOLD_DATA_PATH, "fact_sales.parquet"), index=False)

    # **Particionamento de Vendas Diárias**
    # Adiciona colunas de partição (ano, mês, dia) para organizar os dados
    daily_sales['sale_date'] = pd.to_datetime(daily_sales['sale_date'])
    daily_sales['year'] = daily_sales['sale_date'].dt.year
    daily_sales['month'] = daily_sales['sale_date'].dt.month
    daily_sales['day'] = daily_sales['sale_date'].dt.day

    # Define o caminho para salvar as vendas diárias na camada Gold
    gold_daily_sales_path = os.path.join(GOLD_DATA_PATH, "daily_sales/")
    # Garante que o diretório para vendas diárias particionadas exista
    if not os.path.exists(gold_daily_sales_path):
        os.makedirs(gold_daily_sales_path)
    # Salva os dados particionados por ano/mês/dia no formato Parquet
    daily_sales.to_parquet(gold_daily_sales_path, index=False, partition_cols=['year', 'month', 'day'])

    # Mensagem de sucesso após o processamento
    print("Dados processados e salvos na camada Gold com sucesso.")


ensure_gold_directory_exists()  # Garantir que o diretório Gold exista
process_and_move_to_gold()  # Executar o pipeline Silver → Gold
