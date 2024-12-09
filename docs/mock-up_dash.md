# Monthly Sales Analysis Dashboard

---

## **Filters**

- **Sale Date:** A date range to select the desired sales period.
- **Product Sold:** A text box to search and select specific products.
- **Sales Region:** A dropdown to select one or more regions.

---

### **Overview in Cards**
- **Total Sales (in currency):** The total sales value for the selected period.
- **Total Quantity Sold:** The total number of items sold.
- **Best Performing Month:** The month with the highest sales volume.
- **Best Selling Product:** The name of the top-selling product.
- **Top Performer Seller:** The name of the seller with the highest sales volume.

---

## **Section 2: Monthly Sales**

### **Line Chart**
- **X-Axis:** Months of the year (January, February, etc.).
- **Y-Axis:** Total sales (in currency).
- **Lines:** Different colors for each year to compare trends year over year.

### **Local Filter for This Visual**
- **Year:** Allows selecting one or more years to view comparisons.

---

## **Section 3: Sales by Product**

### **Product Table**
| **Product Name**    | **Quantity Sold** | **Total Sales (in currency)** | **Share of Total (%)** |
|----------------------|-------------------|--------------------------------|------------------------|
| Product A            | 1,000            | 10,000.00                     | 25%                   |
| Product B            | 750              | 7,500.00                      | 18%                   |

### **Horizontal Bar Chart**
- **X-Axis:** Total sales (in currency).
- **Y-Axis:** Product names.
- Displays the **Top 10 Best-Selling Products**.

---

## **Section 4: Sales by Customer**

### **Pie or Donut Chart**
- **Segmentation:** Top 5 customers versus Others.
- Displays the share of customers in total sales.

### **Detailed Table**
| **Customer Name**    | **Region**  | **Quantity Purchased** | **Total Spent (in currency)** |
|-----------------------|------------|-------------------------|------------------------------|
| Customer A            | Southeast  | 500                     | 5,000.00                    |
| Customer B            | Northeast  | 300                     | 3,000.00                    |

---

## **Section 5: Sales by Seller**

### **Seller Table**
| **Seller Name**      | **Quantity Sold** | **Total Sales (in currency)** | **Share of Total (%)** |
|-----------------------|-------------------|--------------------------------|------------------------|
| Seller X             | 1,500            | 15,000.00                     | 30%                   |
| Seller Y             | 1,000            | 10,000.00                     | 20%                   |

### **Vertical Bar Chart**
- **X-Axis:** Seller names.
- **Y-Axis:** Total sales (in currency).

---

## **Interactivity Tools**

### **Dynamic Tooltip**
- Hovering over charts displays details such as:
  - Quantity sold.
  - Cumulative revenue.

### **Export Button**
- Export charts or tables to **CSV**, **PDF**, or **Excel**.

---

## **Recommended Tools**

### **Implementation Tools**
- **Power BI** or **Tableau**: For interactive design and visualization.
- **Amazon QuickSight**: To analyze data stored in S3 or Redshift.

### **Data Connections**
- Integrate **Gold Layer** data directly into the dashboard to ensure insights are based on the most recent processed data.
