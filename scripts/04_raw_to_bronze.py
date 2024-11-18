import pandas as pd
import os

# Definir caminhos para as camadas RAW e BRONZE
RAW_DATA_PATH = "s3/raw/sales_raw.csv"  # Caminho para o arquivo RAW (CSV)
BRONZE_DATA_PATH = "s3/bronze/sales_bronze"  # Diretório base para a camada BRONZE (Parquet)

# Garantir que o diretório da camada Bronze exista
def ensure_bronze_directory_exists():
    if not os.path.exists(BRONZE_DATA_PATH):
        os.makedirs(BRONZE_DATA_PATH)
        print(f"Diretório criado: {BRONZE_DATA_PATH}")
    else:
        print(f"Diretório já existe: {BRONZE_DATA_PATH}")

# Função para adicionar partições
def process_data(df):
    # Converter colunas de data para o formato ISO e criar partições
    if 'sale_date' in df.columns:  # Substitua 'sale_date' pelo nome da sua coluna de data
        df['year'] = df['sale_date'].dt.year              # Criar coluna para o ano
        df['month'] = df['sale_date'].dt.month            # Criar coluna para o mês
        df['day'] = df['sale_date'].dt.day                # Criar coluna para o dia
    else:
        raise ValueError("A coluna 'sale_date' não foi encontrada no dataset.")

    return df

# Função para converter dados de CSV (RAW) para Parquet (BRONZE) com partições
def raw_to_bronze():
    try:
        # Ler os dados da camada RAW (CSV)
        print(f"Lendo dados da camada RAW: {RAW_DATA_PATH}")
        raw_data = pd.read_csv(RAW_DATA_PATH)

        # criar partições 
        print("Processando os dados...")
        processed_data = process_data(raw_data)

        # Salvar os dados na camada BRONZE como Parquet com partições
        print(f"Salvando dados na camada BRONZE (particionado): {BRONZE_DATA_PATH}")
        processed_data.to_parquet(
            BRONZE_DATA_PATH,  # Diretório base
            index=False,
            partition_cols=['year', 'month', 'day']  # Definir partições
        )
        print("Dados processados e salvos no formato Parquet com sucesso.")
    except Exception as e:
        print(f"Erro ao processar os dados: {e}")

ensure_bronze_directory_exists()  # Garantir que o diretório Bronze exista
raw_to_bronze()  # Executar a conversão RAW → BRONZE
