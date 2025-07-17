import streamlit as st
import pandas as pd
import pyodbc

st.subheader("Select Time Range")

start_date = st.date_input("Start date", pd.to_datetime("2025-02-01").date())
start_time_val = st.time_input("Start time", pd.to_datetime("00:05").time())

end_date = st.date_input("End date", pd.Timestamp.now().date())
end_time_val = st.time_input("End time", pd.Timestamp.now().time())

# Combine date and time into full datetime objects
start_datetime = pd.to_datetime(f"{start_date} {start_time_val}")
end_datetime = pd.to_datetime(f"{end_date} {end_time_val}")

# --- Connect to SQL Server ---
@st.cache_data
def load_data(start, end):
    server = 'SAWpAEMO'
    database = 'InfoServer'
    connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    connection = pyodbc.connect(connection_string)

    query  = f"""
    SELECT [SETTLEMENTDATE], [REGIONID], [PERIODID], [RRP]
    FROM [InfoServer].[dbo].[TRADINGPRICE]
    WHERE [REGIONID] = 'SA1'
    AND [SETTLEMENTDATE] BETWEEN '{start.strftime('%Y-%m-%d %H:%M:%S')}' AND '{end.strftime('%Y-%m-%d %H:%M:%S')}'
    """
    df = pd.read_sql_query(query, connection)
    connection.close()
    return df

# --- Load and display data ---
if start_datetime < end_datetime:
    df = load_data(start_datetime, end_datetime)
    st.dataframe(df)
else:
    st.warning("Start time must be before end time.")
