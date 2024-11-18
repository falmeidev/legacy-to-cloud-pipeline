# Proposta: Modelo de Machine Learning no Amazon SageMaker para Previsão de Vendas Futuras

## **1. Objetivo**

Desenvolver um modelo de machine learning para prever vendas futuras (valores ou quantidades) com base em dados históricos. O modelo ajudará a:
- Identificar tendências de vendas.
- Planejar estoques e recursos.
- Melhorar campanhas de marketing.

---

## **2. Dados Necessários**

Os dados devem ser extraídos da **camada Gold**. Para o modelo, serão selecionados os seguintes dados:

| **Coluna**      | **Descrição**                                   |
|------------------|-----------------------------------------------|
| `sale_date`      | Data da venda.                                |
| `total_sales`    | Valor total das vendas.                       |
| `product_id`     | Identificador do produto.                     |
| `customer_id`    | Identificador do cliente.                     |
| `region`         | Região onde a venda foi realizada.            |

---

## **3. Abordagem do Modelo**

### **Modelo Proposto: Regressão Linear e/ou XGBoost**
- **Regressão Linear**:
  - Modelo simples para identificar relações entre o tempo e as vendas.
- **XGBoost**:
  - Algoritmo robusto e eficiente para lidar com dados complexos e múltiplas features.

### **Recursos Adicionais para Melhorar o Modelo**
- **Média Móvel**:
  - Média de vendas nos últimos 7 ou 30 dias.
- **Tendências Sazonais**:
  - Diferença percentual entre o mês atual e o mesmo mês no ano anterior.

---

## **4. Fluxo de Implementação no Amazon SageMaker**

### **Passo 1: Preparação dos Dados**
1. **Fonte dos Dados**:
   - Dados armazenados no Amazon S3 em formato Parquet, já processados e armazenados na camada Gold.
2. **Divisão dos Dados**:
   - **Treino (70%)**: Período histórico.
   - **Validação (15%)**: Período recente para ajustar o modelo.
   - **Teste (15%)**: Para avaliar o desempenho.

---

### **Passo 2: Criação do Notebook no SageMaker**
1. Iniciar um notebook no SageMaker.
2. Conectar ao Amazon S3 para carregar os dados.
3. Usar bibliotecas como **pandas**, **scikit-learn** ou o **XGBoost SDK** para processamento e modelagem.

---

### **Passo 3: Treinamento do Modelo**

Exemplo de código para treinar um modelo de regressão usando XGBoost no SageMaker:

```python
import sagemaker
from sagemaker import get_execution_role
from sagemaker.estimator import Estimator

# Configuração básica
role = get_execution_role()
session = sagemaker.Session()
bucket = 'nome-do-seu-bucket'

# Caminho dos dados
train_data = f's3://{bucket}/dados/treino.csv'
validation_data = f's3://{bucket}/dados/validacao.csv'

# Definição do Estimator para XGBoost
xgboost_estimator = Estimator(
    image_uri=sagemaker.image_uris.retrieve("xgboost", session.boto_region_name, "1.5-1"),
    role=role,
    instance_count=1,
    instance_type="ml.m5.large",
    output_path=f's3://{bucket}/modelos/xgboost/',
    sagemaker_session=session
)

# Hiperparâmetros do XGBoost
xgboost_estimator.set_hyperparameters(
    objective="reg:squarederror",
    num_round=100,
    max_depth=5,
    eta=0.2,
    gamma=4,
    subsample=0.8,
    verbosity=1
)

# Treinamento do modelo
xgboost_estimator.fit({'train': train_data, 'validation': validation_data})
