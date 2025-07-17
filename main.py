import streamlit as st
import pandas as pd
import pyodbc

# --- Title ---
st.title("SA1 Trading Prices Viewer")

# --- Time filter input ---
start_time = st.datetime_input("Start time", pd.to_datetime("2025-02-01 00:05"))
end_time =  st.datetime_input("End time", pd.Timestamp.now())

# --- Connect to SQL Server ---
@st.cache_data
def load_data(start, end):
    server = 'SAWpAEMO'
    database = 'InfoServer'
    connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    connection = pyodbc.connect(connection_string)

    query = f"""
        SELECT [SETTLEMENTDATE], [REGIONID], [PERIODID], [RRP]
        FROM [InfoServer].[dbo].[TRADINGPRICE]
        WHERE [REGIONID] = 'SA1'
        AND [SETTLEMENTDATE] BETWEEN '{start}' AND '{end}'
    """
    df = pd.read_sql_query(query, connection)
    connection.close()
    return df

# --- Load and display data ---
if start_time < end_time:
    df = load_data(start_time, end_time)
    st.dataframe(df)
else:
    st.warning("Start time must be before end time.")
