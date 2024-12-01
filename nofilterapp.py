import streamlit as st
import mysql.connector
import pandas as pd

def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="REDBUS"
    )
    return connection

def fetch_data():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)  
    cursor.execute("SELECT * FROM busdetails")  
    result = cursor.fetchall()  
    connection.close()
    return result

def app():
    st.title('Database Data View')

    st.write('Fetching data from MySQL database...')
    
    data = fetch_data()

    df = pd.DataFrame(data)

    if not df.empty:
        st.write(df)
    else:
        st.write("No data found.")

if __name__ == "__main__":
    app()