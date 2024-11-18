import pandas as pd
import os
import glob

# Definir caminhos para as camadas BRONZE e SILVER
BRONZE_DATA_PATH = "s3/bronze/sales_bronze/"
SILVER_DATA_PATH = "s3/silver/sales_silver/"

# Garantir que o diretório da camada Silver exista
def ensure_silver_directory_exists():
    if not os.path.exists(SILVER_DATA_PATH):
        os.makedirs(SILVER_DATA_PATH)
        print(f"Diretório criado: {SILVER_DATA_PATH}")
    else:
        print(f"Diretório já existe: {SILVER_DATA_PATH}")

# Função para processar dados: converter datas e remover duplicatas
def process_data(df):
    # Converter datas para o formato ISO (YYYY-MM-DD)
    if 'sale_date' in df.columns:  # Substitua 'sale_date' pelo nome da sua coluna de data
        df['sale_date'] = pd.to_datetime(df['sale_date']).dt.strftime('%Y-%m-%d')  # Converter para ISO
    else:
        raise ValueError("A coluna 'sale_date' não foi encontrada no dataset.")

    # Remover duplicatas
    df = df.drop_duplicates()

    return df

# Função para mover dados da camada Bronze para a camada Silver
def bronze_to_silver():
    try:
        # Encontra todos os arquivos Parquet na camada Bronze
        bronze_files = glob.glob(os.path.join(BRONZE_DATA_PATH, "**/*.parquet"), recursive=True)
        
        if not bronze_files:
            raise FileNotFoundError("Nenhum arquivo encontrado na camada Bronze.")

        # Inicializar o DataFrame consolidado
        processed_data = pd.DataFrame()

        for file in bronze_files:
            print(f"Processando arquivo: {file}")
            
            # Ler o arquivo Parquet
            bronze_data = pd.read_parquet(file)

            # Processar os dados
            processed_data = pd.concat([processed_data, process_data(bronze_data)], ignore_index=True)

        # Salvar o DataFrame consolidado na camada Silver
        processed_data.to_parquet(f'{SILVER_DATA_PATH}/sales.parquet', index=False)
        print(f"Dados processados e salvos na camada Silver: {SILVER_DATA_PATH}/sales.parquet")

    except Exception as e:
        print(f"Erro ao mover dados para a camada Silver: {e}")


ensure_silver_directory_exists()  # Garantir que o diretório Silver exista
bronze_to_silver()  # Executar a movimentação BRONZE → SILVER
