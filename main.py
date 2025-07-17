import pandas as pd
import pyodbc
# Establish connection parameters
server = 'SAWpAEMO'
database = 'InfoServer'

# Create a connection string for Windows Authentication
connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# Establish connection
connection = pyodbc.connect(connection_string)

# Create a cursor
cursor = connection.cursor()

# Example query
query1 = "SELECT [SETTLEMENTDATE], [REGIONID], [PERIODID], [RRP]  " \
         "FROM [InfoServer].[dbo].[TRADINGPRICE]  " \
         "where [REGIONID] = 'SA1' and [SETTLEMENTDATE] >= '2025-02-01 00:05'"
df1 = pd.read_sql_query(query1, connection)

print(df1)