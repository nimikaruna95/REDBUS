import streamlit as st
import mysql.connector
import pandas as pd

# Function to create a connection to the MySQL database
def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="REDBUS"
    )
    return connection

# Function to fetch data from the database
def fetch_data():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM busdetails")
    result = cursor.fetchall()
    connection.close()
    return result

# Basic CSS styles
st.markdown("""
    <style>
    body {
        background-color: #f7f7f7;
    }
    .stTitle {
        color: #2E4A6D;
        font-size: 36px;
    }      
    .stSubheader {
        color: #2E4A6D;
        font-size: 24px;
        margin-top: 20px;
    }
    .stDataFrame {
        border: 1px solid black;
        background-color:white;
    }
    .sidebar .sidebar-content {
        background-color: #f0f4f8;
    }
    .sidebar .sidebar-header {
        background-color: #2E4A6D;
        color: white;
        font-size: 20px;
        padding: 10px;
    }
    .sidebar select,
    .sidebar .stSelectbox,
    .sidebar .stSlider {
        background-color: #e1f0f8;
        border: 1px solid #2E4A6D;
        border-radius: 5px;
        padding: 10px;
        font-size: 14px;
        color: #2E4A6D;
    }
    .sidebar select:focus,
    .sidebar .stSelectbox:focus,
    .sidebar .stSlider:focus {
        outline: none;
        border-color: #1A3F6C;
    }
    .stSlider>div>div {
        padding: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit app function
def app():
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
    # State_name filter
    state_filter = st.sidebar.selectbox("Select State", df["State_name"].unique())
    df_filtered = df[df["State_name"] == state_filter]

    # Bus_type filter
    bustype_filter = st.sidebar.selectbox("Select Bustype", ["All"] + df_filtered["Bustype"].unique().tolist())
    if bustype_filter != "All":
        df_filtered = df_filtered[df_filtered["Bustype"] == bustype_filter]

    # Route_name filter
    route_filter = st.sidebar.selectbox("Select Route Name", ["All"] + df_filtered["Route_names"].unique().tolist())
    if route_filter != "All":
        df_filtered = df_filtered[df_filtered["Route_names"] == route_filter]

    # Route_link filter
    route_links_filter = st.sidebar.selectbox("Select Route Link", ["All"] + df_filtered["Route_links"].unique().tolist())
    if route_links_filter != "All":
        df_filtered = df_filtered[df_filtered["Route_links"] == route_links_filter]

    # Star_rating filter
    star_rating_range = st.sidebar.slider("Select Star Rating Range", min_value=0.0, max_value=5.0, value=(0.0, 5.0), step=0.1)
    df_filtered = df_filtered[(df_filtered["Star_rating"] >= star_rating_range[0]) & (df_filtered["Star_rating"] <= star_rating_range[1])]

    # Seats filter
    seats_range = st.sidebar.slider("Select Seats Available Range", min_value=0, max_value=60, value=(0, 100), step=1)
    df_filtered = df_filtered[(df_filtered["Seats_available"] >= seats_range[0]) & (df_filtered["Seats_available"] <= seats_range[1])]

    # Price filter
    price_range = st.sidebar.slider("Select Price Range", min_value=0.0, max_value=5000.0, value=(0.0, 7000.0), step=100.0)
    df_filtered = df_filtered[(df_filtered["Price"] >= price_range[0]) & (df_filtered["Price"] <= price_range[1])]

    st.subheader(f"Bus Routes in {state_filter}")
    if df_filtered.empty:
        st.write("No data available for the selected filters.")
    else:
        st.dataframe(df_filtered, use_container_width=True)

if __name__ == "__main__":
    app()
