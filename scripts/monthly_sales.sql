-- Seleciona dados agregados de vendas mensais com base em tabelas fato e dimensionais
SELECT 
    d.year, -- Ano da venda, extraído da dimensão de datas (dim_date)
    d.month, -- Mês da venda, extraído da dimensão de datas (dim_date)
    c.customer_name, -- Nome do cliente, extraído da dimensão de clientes (dim_customer)
    p.product_name, -- Nome do produto, extraído da dimensão de produtos (dim_product)
    s.seller_name, -- Nome do vendedor, extraído da dimensão de vendedores (dim_seller)
    SUM(f.total_value) AS total_sales, -- Soma do valor total de vendas para o agrupamento especificado
    SUM(f.quantity) AS total_quantity -- Soma da quantidade total de itens vendidos no agrupamento especificado
FROM 
    fact_sales f -- Tabela fato que contém as transações de vendas
JOIN 
    dim_date d ON f.sale_date = d.sale_date -- Relaciona a tabela fato à dimensão de datas pelo campo 'sale_date'
JOIN 
    dim_customer c ON f.customer_id = c.customer_id -- Relaciona a tabela fato à dimensão de clientes pelo 'customer_id'
JOIN 
    dim_product p ON f.product_id = p.product_id -- Relaciona a tabela fato à dimensão de produtos pelo 'product_id'
JOIN 
    dim_seller s ON f.seller_id = s.seller_id -- Relaciona a tabela fato à dimensão de vendedores pelo 'seller_id'
GROUP BY 
    d.year, -- Agrupa os resultados por ano
    d.month, -- Agrupa os resultados por mês
    c.customer_name, -- Agrupa os resultados por nome do cliente
    p.product_name, -- Agrupa os resultados por nome do produto
    s.seller_name -- Agrupa os resultados por nome do vendedor
ORDER BY 
    d.year, -- Ordena os resultados primeiro por ano
    d.month, -- Ordena os resultados depois por mês
    total_sales DESC; -- Ordena dentro de cada mês pelos maiores valores de vendas
