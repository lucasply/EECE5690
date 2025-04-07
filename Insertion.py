# Relevant Libraries
import mysql.connector
import pandas as pd
import numpy as np

# Connect to DB
connection = mysql.connector.connect(host='localhost',
                                         database='Project',
                                         user='root',
                                         password='Password')

cursor = connection.cursor()

# Inserting data into our database
