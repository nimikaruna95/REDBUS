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
    st.markdown("""
    <style>
        body {
            background-color: #f4f4f9;
        }

        .title {
            font-size: 20px;
            font-weight: bold;
            color: Red;
            text-align: center;
            margin-top:0 px;
        }

        .header {
            font-size: 18px;
            font-weight: normal;
            color: #4CAF50;
            text-align: center;
        }

        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
        }

        .stSelectbox, .stSlider, .stTextInput, .stCheckbox {
            border-radius: 5px;
            background-color: #ffffff;
        }

        .sidebar .sidebar-content {
            background-color: #ffffff;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 title="Redbus"></h1>', unsafe_allow_html=True)
    st.title('RedBus')
    st.write('Fetching data from MySQL database...')

    data = fetch_data()

    df = pd.DataFrame(data)

    if not df.empty:
        st.write("Data fetched successfully.")
    else:
        st.write("No data found.")
        return

    st.sidebar.header("Filter Options")
    state_filter = st.sidebar.selectbox("Select State", df["State_name"].unique())
    df_filtered = df[df["State_name"] == state_filter]
    
    bustype_filter = st.sidebar.selectbox("Select Bustype", ["All"] + df_filtered["Bustype"].unique().tolist())
    if bustype_filter != "All":
        df_filtered = df_filtered[df_filtered["Bustype"] == bustype_filter]

    route_filter = st.sidebar.selectbox("Select Route Name", ["All"] + df_filtered["Route_names"].unique().tolist())
    if route_filter != "All":
        df_filtered = df_filtered[df_filtered["Route_names"] == route_filter]
        st.markdown(f'<div style="color: blue; font-size: 18px;">{route_filter}</div>', unsafe_allow_html=True)

    route_links_filter = st.sidebar.selectbox("Select Route Link", ["All"] + df_filtered["Route_links"].unique().tolist())
    if route_links_filter != "All":
        df_filtered = df_filtered[df_filtered["Route_links"] == route_links_filter]
        
    star_rating_range = st.sidebar.slider("Select Star Rating Range", min_value=0.0, max_value=5.0, value=(0.0, 5.0), step=0.1)
    df_filtered = df_filtered[(df_filtered["Star_rating"] >= star_rating_range[0]) & (df_filtered["Star_rating"] <= star_rating_range[1])]
    
    seats_range = st.sidebar.slider("Select Seats Available Range", min_value=0, max_value=60, value=(0, 100), step=1)
    df_filtered = df_filtered[(df_filtered["Seats_available"] >= seats_range[0]) & (df_filtered["Seats_available"] <= seats_range[1])]
    
    price_range = st.sidebar.slider("Select Price Range", min_value=0.0, max_value=5000.0, value=(0.0, 5000.0), step=100.0)
    df_filtered = df_filtered[(df_filtered["Price"] >= price_range[0]) & (df_filtered["Price"] <= price_range[1])]
    
    busname_filter = st.sidebar.selectbox("Select Bus Name", ["All"] + df_filtered["Busname"].unique().tolist())
    if busname_filter != "All":
        df_filtered = df_filtered[df_filtered["Busname"] == busname_filter]
       
    st.subheader(f"Bus Routes in {state_filter}")
    if df_filtered.empty:
        st.write("No data available for the selected filters.")
    else:
        st.dataframe(df_filtered)

if __name__ == "__main__":
    app()
