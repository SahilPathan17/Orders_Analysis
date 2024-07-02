#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[5]:


df = pd.read_csv('C:\\Users\\Lab-02-06\\Downloads\\orders.csv',na_values=['Not Available','unknown'])
df['Ship Mode'].unique()


# In[6]:


df.isnull().sum()


# In[7]:


df.head()


# In[8]:


df.rename(columns={'Order Id':'order_id', 'City':'city'})
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ','_')


# In[9]:


df['discount']=df['list_price']*df['discount_percent']*.01  
df['sale_price']=df['list_price']-df['discount_percent']
df['profit']=df['sale_price']-df['cost_price']
df


# In[10]:


df['order_date'] = pd.to_datetime(df['order_date'],format = "%Y-%m-%d")


# In[11]:


df.drop(columns=['list_price','cost_price','discount_percent'],inplace=True)


# In[12]:


df.head()


# In[13]:


pip install PyMySQL


# In[14]:


# load the data into sql server using replace option
import sqlalchemy as sal
# engine = sal.create_engine('mssql://ANKIT\SQLEXPRESS/master?drive=ODBC+Driver+17+for+SQL+Server')
# conn = engine.connect()

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

# Create the engine
engine = create_engine(connection_url)

# Test the connection
try:
    connection = engine.connect()
    print("Connection successful!")
    connection.close()
except Exception as e:
    print(f"Connection failed: {e}")


# In[16]:


df.to_sql('df_orders',con=engine,index=False,if_exists='append')


# In[ ]:


use sakila;
select * from actor;

select concat(first_name," ",last_name) as ename from actor;

select concat (
		upper(left(first_name,1)),lower(substring(first_name,2)) , " " , 
        upper(left(last_name,1)),lower(substring(last_name,2))
    ) as newname
    from actor;
    
#find top 10 highest revenue generating products
select top 10 product_id, sum(sale_price) as sales
from df_orders
group by product_id
order by sales desc

#find top 5 highest selling products in each region
with cte as(select region,product_id,sum(sale_price) as sales
from df_orders
group by region,product_id)
select * from(
select * 
,row_number() over(partition by region order by sales desc) as rn
from cte)A
where rn<=5
--find month over month growth comparison for 2022 and 2023 sales eg
with cte as(
select year(order_date)as order_year,month(order_date) as order_month
    
    
    select 5 product_id,sum(sale_price) as sales 
from df_orders 
group by product_id 
order by sales desc

with cte as (
select region, product_id,sum(sale_price) as sales 
from df_orders 
group by region, product_id
)
select * from (
select *
row_number() over (partition by region order by sales desc) as rn
from cte
)
where rn <= 5
with cte as(
select year(order_date) as order_year, month(order_date) as order_month,
sum(sale_price) as sales
from df_orders
group by year(order_date), month(order_date)
)
select order_month
, sum(case when order_year=2022 then sales else 0 end) as sales_2022
, sum(case when order_year=2023 then sales else 0 end) as sales_2023
from cte
group by order_month
order by order_month

