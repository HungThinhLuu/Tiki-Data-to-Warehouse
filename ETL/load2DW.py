import pandas as pd
from dotenv import load_dotenv
import mysql.connector
import os
load_dotenv()

config = {
  'user': os.getenv('USERNAME'),
  'password': os.getenv('PASSWORD'),
  'host': os.getenv('HOSTNAME'),
  'database': os.getenv('DATABASE'),
}

# import the module
from sqlalchemy import create_engine

# create sqlalchemy engine
engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                       .format(user=os.getenv('USERNAME'),
                               pw=os.getenv('PASSWORD'),
                               host=os.getenv('HOSTNAME'),
                               db=os.getenv('DATABASE')))

data = pd.read_csv('product.csv')
data = data.iloc[data['id'].drop_duplicates().index]
print(data.info())

category = data[['id_category', 'primary_category_name', 'category_path']].drop_duplicates()
category.columns = ['CategoryID', 'Name', 'CategoryPath']
category = category.set_index('CategoryID')

print(category)
category.to_sql('Category_Dim', con = engine, if_exists = 'append', chunksize = 1000)

product = data[['id', 'id_category', 'name', 'original_price', 'rating_average', 'review_count']].drop_duplicates()
product.columns = ['ProductID', 'CategoryID', 'Name', 'Price', 'Rating', 'ReviewCount']
product = product.set_index('ProductID')

print(product.head(5))
product.to_sql('Product_Dim', con = engine, if_exists = 'append', chunksize = 1000)