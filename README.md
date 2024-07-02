# Orders_Analysis

This project involves analyzing order data to derive various insights, including revenue generation, top-selling products, and month-over-month growth. The analysis covers data cleaning, transformation, and storage, followed by querying the data to extract meaningful insights.

<p>

---

## Project Overview

The Order Analysis project involves several key steps:

1. **Data Loading and Initial Exploration**:
    - The dataset is loaded using `pandas`, with specific values treated as missing (`na_values`).
    - The initial data is explored by checking for missing values and displaying the first few rows.

2. **Data Cleaning and Transformation**:
    - Columns are renamed and converted to lower case with underscores replacing spaces for consistency.
    - New columns are created to calculate the discount, sale price, and profit for each order.
    - The `order_date` column is converted to a datetime format for time-based analysis.
    - Unnecessary columns are dropped to simplify the dataset.

3. **Data Storage**:
    - The cleaned data is loaded into a MySQL database using SQLAlchemy and PyMySQL.
    - The connection to the database is tested to ensure successful data loading.

4. **Data Analysis Using SQL**:
    - SQL queries are used to analyze the data stored in the MySQL database.
    - Key queries include:
        - Finding the top 10 highest revenue-generating products.
        - Identifying the top 5 highest-selling products in each region.
        - Calculating month-over-month sales growth for 2022 and 2023.

## Code Breakdown

### Data Loading and Initial Cleaning
```python
import pandas as pd

df = pd.read_csv('C:\\Users\\Lab-02-06\\Downloads\\orders.csv', na_values=['Not Available', 'unknown'])
df['Ship Mode'].unique()
df.isnull().sum()
df.head()

df.rename(columns={'Order Id': 'order_id', 'City': 'city'})
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')
```

### Data Transformation
```python
df['discount'] = df['list_price'] * df['discount_percent'] * 0.01  
df['sale_price'] = df['list_price'] - df['discount_percent']
df['profit'] = df['sale_price'] - df['cost_price']
df['order_date'] = pd.to_datetime(df['order_date'], format="%Y-%m-%d")
df.drop(columns=['list_price', 'cost_price', 'discount_percent'], inplace=True)
```

### Data Storage
```python
import sqlalchemy as sal
from sqlalchemy import create_engine
import pymysql 

# Connection details
username = 'root'
password = 'root'
server = 'localhost'
port = '3306'
dbname = 'sakila'

# Create the connection URL
connection_url = f'mysql+pymysql://{username}:{password}@{server}:{port}/{dbname}'
engine = create_engine(connection_url)

# Test the connection
try:
    connection = engine.connect()
    print("Connection successful!")
    connection.close()
except Exception as e:
    print(f"Connection failed: {e}")

df.to_sql('df_orders', con=engine, index=False, if_exists='append')
```

### Data Analysis Using SQL
```sql
-- Find top 10 highest revenue-generating products
SELECT product_id, SUM(sale_price) AS sales
FROM df_orders
GROUP BY product_id
ORDER BY sales DESC
LIMIT 10;

-- Find top 5 highest-selling products in each region
WITH cte AS (
    SELECT region, product_id, SUM(sale_price) AS sales
    FROM df_orders
    GROUP BY region, product_id
)
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER(PARTITION BY region ORDER BY sales DESC) AS rn
    FROM cte
) A
WHERE rn <= 5;

-- Month-over-month growth comparison for 2022 and 2023 sales
WITH cte AS (
    SELECT YEAR(order_date) AS order_year, MONTH(order_date) AS order_month, SUM(sale_price) AS sales
    FROM df_orders
    GROUP BY YEAR(order_date), MONTH(order_date)
)
SELECT order_month,
       SUM(CASE WHEN order_year = 2022 THEN sales ELSE 0 END) AS sales_2022,
       SUM(CASE WHEN order_year = 2023 THEN sales ELSE 0 END) AS sales_2023
FROM cte
GROUP BY order_month
ORDER BY order_month;
```

## Conclusion

This analysis of the order dataset provides insights into the top-performing products, regional sales trends, and temporal sales patterns. The use of SQL for querying the cleaned data stored in a MySQL database enables efficient and flexible data analysis.

## Future Work

- Further analysis can be conducted to understand customer demographics and their purchasing behavior.
- Machine learning models can be developed to predict future sales based on historical data.

---

</p>
