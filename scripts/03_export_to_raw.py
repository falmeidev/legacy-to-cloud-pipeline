import psycopg2
import os
import csv
from config import DB_CONFIG


# Diretório que simula o bucket S3 local
RAW_DATA_DIR = "s3/raw"

# Função para garantir que o diretório RAW exista
def ensure_raw_directory_exists():
    if not os.path.exists(RAW_DATA_DIR):
        os.makedirs(RAW_DATA_DIR)
        print(f"Diretório criado: {RAW_DATA_DIR}")
    else:
        print(f"Diretório já existe: {RAW_DATA_DIR}")

# Função para extrair dados do PostgreSQL e salvar como CSV
def export_data_to_raw():
    try:
        # Conectar ao banco de dados
        conn = psycopg2.connect(**DB_CONFIG)
        # Cria um cursor para executar comandos SQL no banco
        cursor = conn.cursor()

        # Consulta SQL para extrair todos os dados da tabela 'sales'
        query = "SELECT * FROM sales;"
         # Executa a consulta no banco de dados
        cursor.execute(query)
        # Retorna uma lista de tuplas, onde cada tupla é uma linha da tabela
        rows = cursor.fetchall()
        # Obtém os nomes das colunas da tabela consultada
        # 'cursor.description' contém metadados das colunas retornadas pela consulta
        columns = [desc[0] for desc in cursor.description]
        
        # Define o caminho para o arquivo CSV na camada RAW
        # 'RAW_DATA_DIR' deve ser definido anteriormente no código e aponta para o diretório RAW no sistema de arquivos
        raw_file_path = os.path.join(RAW_DATA_DIR, "sales_raw.csv")
        # Abre um arquivo CSV para escrita no caminho definido
        # 'newline=""' evita linhas em branco extras em alguns sistemas
        # 'encoding="utf-8"' garante a compatibilidade com caracteres especiais
        with open(raw_file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file) # Cria um objeto escritor CSV
            writer.writerow(columns)  # Escreve o cabeçalho no arquivo (nomes das colunas)
            writer.writerows(rows)   # Escreve os dados extraídos no arquivo
        # Imprime uma mensagem indicando o sucesso da exportação
        print(f"Dados exportados com sucesso para: {raw_file_path}")

    # Tratamento de exceções para capturar erros durante a execução
    except Exception as e:
        print(f"Erro ao exportar dados: {e}")

    # Bloco finally para garantir o fechamento de recursos mesmo em caso de erro
    finally:
        # Fechar conexão com o banco
        if cursor:
            cursor.close()
        if conn:
            conn.close()

ensure_raw_directory_exists()  # Garantir que o diretório RAW existe
export_data_to_raw()           # Exportar os dados para o diretório RAW
