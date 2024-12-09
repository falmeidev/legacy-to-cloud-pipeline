# Proposal: Machine Learning Model on Amazon SageMaker for Future Sales Forecasting

## **1. Objective**

Develop a machine learning model to forecast future sales (values or quantities) based on historical data. The model aims to:
- Identify sales trends.
- Plan inventory and resources.
- Enhance marketing campaigns.

---

## **2. Required Data**

Data will be extracted from the **Gold layer**. The selected features for the model include:

| **Column**      | **Description**                              |
|------------------|---------------------------------------------|
| `sale_date`      | Sale date.                                  |
| `total_sales`    | Total sales value.                          |
| `product_id`     | Product identifier.                         |
| `customer_id`    | Customer identifier.                        |
| `region`         | Region where the sale occurred.             |

---

## **3. Model Approach**

### **Proposed Models: Linear Regression and/or XGBoost**
- **Linear Regression**:
  - A simple model to identify relationships between time and sales.
- **XGBoost**:
  - A robust and efficient algorithm for handling complex data with multiple features.

### **Additional Features to Improve the Model**
- **Moving Average**:
  - Average sales over the last 7 or 30 days.
- **Seasonal Trends**:
  - Percentage difference between the current month and the same month in the previous year.

---

## **4. Implementation Workflow on Amazon SageMaker**

### **Step 1: Data Preparation**
1. **Data Source**:
   - Data stored in Amazon S3 in Parquet format, processed and stored in the Gold layer.
2. **Data Splitting**:
   - **Training (70%)**: Historical period.
   - **Validation (15%)**: Recent period to adjust the model.
   - **Testing (15%)**: To evaluate performance.

---

### **Step 2: Creating a Notebook in SageMaker**
1. Launch a notebook in SageMaker.
2. Connect to Amazon S3 to load the data.
3. Use libraries like **pandas**, **scikit-learn**, or the **XGBoost SDK** for data processing and modeling.

---

### **Step 3: Model Training**

Example code for training a regression model using XGBoost in SageMaker:

```python
import sagemaker
from sagemaker import get_execution_role
from sagemaker.estimator import Estimator

# Basic configuration
role = get_execution_role()
session = sagemaker.Session()
bucket = 'your-bucket-name'

# Data paths
train_data = f's3://{bucket}/data/train.csv'
validation_data = f's3://{bucket}/data/validation.csv'

# Define the XGBoost Estimator
xgboost_estimator = Estimator(
    image_uri=sagemaker.image_uris.retrieve("xgboost", session.boto_region_name, "1.5-1"),
    role=role,
    instance_count=1,
    instance_type="ml.m5.large",
    output_path=f's3://{bucket}/models/xgboost/',
    sagemaker_session=session
)

# Set XGBoost hyperparameters
xgboost_estimator.set_hyperparameters(
    objective="reg:squarederror",
    num_round=100,
    max_depth=5,
    eta=0.2,
    gamma=4,
    subsample=0.8,
    verbosity=1
)

# Train the model
xgboost_estimator.fit({'train': train_data, 'validation': validation_data})
