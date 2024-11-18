import psycopg2
from config import DB_CONFIG

# Função para criar o banco de dados 'legacy_sales_db' caso ele ainda não exista
def create_database():
    try:
        # Conecta ao servidor PostgreSQL utilizando as configurações definidas em 'DB_CONFIG'
        # 'DB_CONFIG' deve conter informações como host, usuário, senha e porta.
        conn = psycopg2.connect(**DB_CONFIG)
        # Ativa o modo de autocommit, necessário para executar comandos como CREATE DATABASE.
        # Sem autocommit, o comando seria parte de uma transação, o que não é permitido para CREATE DATABASE.
        conn.autocommit = True  
        # Cria um cursor para executar comandos SQL no servidor PostgreSQL.
        cursor = conn.cursor()
        
        # Verifica se o banco de dados 'legacy_sales_db' já existe.
        # A consulta SELECT 1 retorna uma linha se o banco existir, caso contrário, não retorna nada.
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'legacy_sales_db'")
        # Se o cursor não retornar nenhum resultado, significa que o banco não existe.
        if not cursor.fetchone():
            # Cria o banco de dados 'legacy_sales_db' caso ele não exista.
            cursor.execute("CREATE DATABASE legacy_sales_db")
            print("Banco de dados 'legacy_sales_db' criado com sucesso.")
        else:
            # Informa que o banco já existe e não é necessário criá-lo.
            print("Banco de dados 'legacy_sales_db' já existe.")

    # Captura qualquer exceção que possa ocorrer durante o processo de conexão ou execução de comandos.    
    except Exception as e:
        print("Erro ao criar o banco de dados:", e)
    
    # Bloco 'finally' é usado para garantir que os recursos sejam liberados adequadamente,
    # independentemente de sucesso ou falha no bloco 'try'.
    finally:
        if cursor:  # Verifica se o cursor foi inicializado
            cursor.close() # Fecha o cursor para liberar recursos
        if conn:  # Verifica se a conexão foi estabelecida
            conn.close() # Fecha a conexão com o banco de dados

# Executa a função create_database
create_database()
