# Dashboard de Análise de Vendas Mensais

---

## **Filtros**

- **Data da Venda:** Data range que permite selecionar o período desejado das vendas.
- **Produto Vendido:** Caixa de texto que permite pesquisar e selecionar os produtos desejados.
- **Região da Venda:** Dropdown com as opções de regiões, que permita secionar 1 ou mais regiões.

---

### **Visão Geral em Cards**
- **Total de Vendas (R$):** Valor total de vendas no período selecionado.
- **Quantidade Total Vendida:** Total de itens vendidos.
- **Mês de Melhor Desempenho:** Mês com maior volume de vendas.
- **Produto Mais Vendido:** Nome do produto mais vendido.
- **Vendedor Top Performer:** Nome do vendedor com maior volume de vendas.

---

## **Seção 2: Vendas por Mês**

### **Gráfico de Linhas**
- **Eixo X:** Meses do ano (Janeiro, Fevereiro, etc).
- **Eixo Y:** Total de vendas (em R$).
- **Linhas:** Diferentes cores para cada ano, permitindo comparar tendências ano a ano.

### **Filtro local para este visual**
- **Ano:** Permitir selecionar um ou mais anos para visualizar a comparação.

---

## **Seção 3: Vendas por Produto**

### **Tabela de Produtos**
| **Nome do Produto** | **Quantidade Vendida** | **Total de Vendas (R$)** | **Participação no Total (%)** |
|----------------------|------------------------|---------------------------|-------------------------------|
| Produto A            | 1.000                 | 10.000,00                | 25%                           |
| Produto B            | 750                   | 7.500,00                 | 18%                           |

### **Gráfico de Barras Horizontal**
- **Eixo X:** Total de vendas (em R$).
- **Eixo Y:** Nome dos produtos.
- Mostra os **Top 10 produtos mais vendidos**.

---

## **Seção 4: Vendas por Cliente**

### **Gráfico de Pizza ou Donut**
- **Segmentação:** Top 5 clientes versus Outros.
- Mostra a participação dos clientes no total de vendas.

### **Tabela Detalhada**
| **Nome do Cliente** | **Região**  | **Quantidade Comprada** | **Total Gasto (R$)** |
|----------------------|------------|--------------------------|-----------------------|
| Cliente A            | Sudeste    | 500                      | 5.000,00             |
| Cliente B            | Nordeste   | 300                      | 3.000,00             |

---

## **Seção 5: Vendas por Vendedor**

### **Tabela de Vendedores**
| **Nome do Vendedor** | **Quantidade Vendida** | **Total de Vendas (R$)** | **Participação no Total (%)** |
|-----------------------|------------------------|---------------------------|-------------------------------|
| Vendedor X            | 1.500                 | 15.000,00                | 30%                           |
| Vendedor Y            | 1.000                 | 10.000,00                | 20%                           |

### **Gráfico de Barras Vertical**
- **Eixo X:** Nome dos vendedores.
- **Eixo Y:** Total de vendas (em R$).

---

## **Ferramentas de Interatividade**

### **Tooltip Dinâmico**
- Ao passar o cursor sobre gráficos, exibir detalhes como:
  - Quantidade vendida.
  - Faturamento acumulado.

### **Botão de Exportação**
- Exportar gráficos ou tabelas para **CSV**, **PDF** ou **Excel**.

---

## **Ferramentas Recomendadas**

### **Ferramentas para Implementação**
- **Power BI** ou **Tableau**: Para design e visualização interativa.
- **Amazon QuickSight**: analisar dados armazenados no S3 ou Redshift.

### **Conexões com Dados**
- Integrar os dados da camada **Gold** diretamente ao dashboard para garantir que os insights sejam baseados nos dados processados mais recentes.
