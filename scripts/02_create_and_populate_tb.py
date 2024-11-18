import psycopg2
from datetime import datetime, timedelta
import random
from config import DB_CONFIG

# Função para gerar dados fictícios de vendas
def generate_sales_data(num_records=500):
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    products = list(range(101, 111))
    regions = ['Norte', 'Sul', 'Leste', 'Oeste', 'Centro']
    
    sales_data = []
    for _ in range(num_records):
        sale_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        product_id = random.choice(products)
        customer_id = random.randint(1001, 2000)
        quantity = random.randint(1, 10)
        unit_price = round(random.uniform(10.0, 100.0), 2)
        total_value = round(quantity * unit_price, 2)
        seller_id = random.randint(1, 20)
        region = random.choice(regions)
        
        sale = (sale_date.strftime('%Y-%m-%d'), product_id, customer_id, quantity, unit_price, total_value, seller_id, region)
        sales_data.append(sale)
    return sales_data

# Função para criar a tabela e inserir os dados
def create_and_insert_sales():
    conn = None  # Inicializa a variável de conexão
    cursor = None  # Inicializa a variável do cursor
    try:
        # Conectar ao banco de dados PostgreSQL usando as configurações armazenadas em DB_CONFIG
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Comando SQL para criar a tabela 'sales' se ela ainda não existir
        create_table_query = """
        CREATE TABLE IF NOT EXISTS sales (
            id SERIAL PRIMARY KEY,
            sale_date DATE NOT NULL,
            product_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price DECIMAL(10,2) NOT NULL,
            total_value DECIMAL(10,2) NOT NULL,
            seller_id INTEGER NOT NULL,
            region VARCHAR(50) NOT NULL
        );
        """
        # Executa o comando SQL para criar a tabela
        cursor.execute(create_table_query)
        # Confirma a criação da tabela no banco de dados
        conn.commit()
        print("Tabela 'sales' criada com sucesso.")
        
        # Gera dados fictícios para inserir na tabela
        sales_data = generate_sales_data(500)
        
        # Inserir os dados gerados
        insert_query = """
        INSERT INTO sales (sale_date, product_id, customer_id, quantity, unit_price, total_value, seller_id, region)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Insere os dados gerados na tabela usando executemany, que permite múltiplos inserts em uma única operação
        cursor.executemany(insert_query, sales_data)
        # Confirma a inserção dos dados no banco
        conn.commit()
        print(f"{cursor.rowcount} registros inseridos com sucesso.")
    
    # Tratamento de exceções para capturar erros durante a execução
    except Exception as e:
        # Exibe a mensagem de erro
        print("Erro:", e)
    
    # Bloco finally para garantir o fechamento de recursos mesmo em caso de erro
    finally:
        # Fechar cursor e conexão, se foram criados
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

# Chama a função para criar a tabela e inserir os dados
create_and_insert_sales()
