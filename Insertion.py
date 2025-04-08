# Relevant Libraries
import mysql.connector
import pandas as pd
import numpy as np

# Connect to DB
connection = mysql.connector.connect(
    host='localhost',
    database='Project',
    user='root',
    password='Password!'
)
cursor = connection.cursor()

# Insert data in Transaction table
df = pd.read_csv('CSV/Transactions.csv') 
df = df.replace(np.nan, None)  

df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date

for row in df.itertuples(index=False):
    data = (row.CustomerID, row.TransactionNum, row.TransactionID, row.Date)
    cursor.execute("""INSERT IGNORE INTO `Transaction` (CustomerID, TransactionNum, TransactionId, date)
                      VALUES (%s, %s, %s, %s)""", data)

# Commit the changes
connection.commit()

# Insert data in Customer table
df = pd.read_csv('CSV/Customer_Data.csv')
df = df.replace(np.nan, None)

for row in df.itertuples(index=False):
    data = (row.CustomerID, row.name, row.address, row.age, row.gender)
    cursor.execute("""INSERT IGNORE INTO Customer (CustomerID, name, address, age, gender)
                  VALUES (%s, %s, %s, %s, %s)""", data)
connection.commit()

# Insert data in Product table
df = pd.read_csv('CSV/Product_Data.csv')
df = df.replace(np.nan, None)
# CustomerID,TransactionId,ProductId,ProductType,quantity,price
# Compute total pre-tax and post-tax per transaction


for row in df.itertuples(index=False):
    data = (row.CustomerID, row.TransactionId, row.ProductId, row.ProductType, row.quantity, row.price)
    cursor.execute("""INSERT IGNORE INTO Product (CustomerID, TransactionId, ProductId, ProductType, quantity, price)
                    VALUES (%s, %s, %s, %s, %s, %s)""", data)
connection.commit()

# Compute total pre-tax and post-tax per transaction
tax_rate = 1.10
df['line_total'] = df['quantity'] * df['price']

totals = df.groupby('TransactionId')['line_total'].sum().reset_index()
totals['TotalPreTax'] = totals['line_total']
totals['TotalPostTax'] = totals['line_total'] * tax_rate
totals = totals.drop(columns=['line_total'])

for row in totals.itertuples(index=False):
    data = (row.TotalPreTax, row.TotalPostTax, row.TransactionId)
    cursor.execute("""UPDATE `Transaction`
                      SET TotalPreTax = %s, TotalPostTax = %s
                      WHERE TransactionId = %s""", data)


# Insert data into employee table
df = pd.read_csv('CSV/Employee.csv')
df = df.replace(np.nan, None)

for row in df.itertuples(index=False):
    data = (row.Id, row.Role, row.Department)
    cursor.execute("""INSERT IGNORE INTO emp (Id, Role, Department)
                    VALUES (%s, %s, %s)""", data)
connection.commit()

# Insert data into Supervisor table
df = pd.read_csv('CSV/Supervisors.csv')
df = df.replace(np.nan, None)

for row in df.itertuples(index=False):
    data = (row.Id, row.SupervisorID, row.Role, row.Dept)
    cursor.execute("""INSERT IGNORE INTO supervisor (Id, SupervisorID, Role, Department)
                    VALUES (%s, %s, %s, %s)""", data)
    
connection.commit()

print("Data has been inserted")
cursor.close()
connection.close()
