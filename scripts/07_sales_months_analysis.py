import pandas as pd
import os

# Caminho para a camada Gold
GOLD_DATA_PATH = "s3/gold/daily_sales/"

def calculate_monthly_sales(gold_data_path):
    try:
        # Carregar todos os arquivos Parquet da camada Gold
        gold_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(gold_data_path) for f in filenames if f.endswith('.parquet')]

        #print(gold_files)
        
        if not gold_files:
            print("Nenhum arquivo Parquet encontrado na camada Gold.")
            return

        # Ler os arquivos Parquet em um único DataFrame
        df = pd.concat([pd.read_parquet(file) for file in gold_files], ignore_index=True)

        # Converter a coluna 'sale_date' para datetime se necessário
        if not pd.api.types.is_datetime64_any_dtype(df['sale_date']):
            df['sale_date'] = pd.to_datetime(df['sale_date'])

        # Criar colunas auxiliares para ano e mês
        df['year'] = df['sale_date'].dt.year
        df['month'] = df['sale_date'].dt.month

        # Agregar por ano e mês
        monthly_sales = df.groupby(['year', 'month']).agg(
            total_sales=('total_sales', 'sum'),
            total_quantity=('total_quantity', 'sum')
        ).reset_index()

        # Ordenar os resultados por ano e mês
        monthly_sales = monthly_sales.sort_values(by=['year', 'month'])

        print("Total de vendas mensais:")
        print(monthly_sales)

        return monthly_sales
    # Captura qualquer exceção que possa ocorrer durante o processo de conexão ou execução de comandos.
    except Exception as e:
        print(f"Erro ao calcular as vendas mensais: {e}")

# Calcula o total de vendas mensal
monthly_sales = calculate_monthly_sales(GOLD_DATA_PATH)


