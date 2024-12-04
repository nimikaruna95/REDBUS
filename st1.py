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
    st.title('RedBus Route Filter')

    st.write('Fetching data from MySQL database...')

    data = fetch_data()

    df = pd.DataFrame(data)

    if not df.empty:
        st.write("Data fetched successfully.")
    else:
        st.write("No data found.")
        return

    st.sidebar.header("Filter Options")

    #State_name
    state_filter = st.sidebar.selectbox("Select State", df["State_name"].unique())
    df_filtered = df[df["State_name"] == state_filter]

    #bus_type
    bustype_filter = st.sidebar.multiselect("Select Bustypes", df_filtered["Bustype"].unique())
    if bustype_filter:
        df_filtered = df_filtered[df_filtered["Bustype"].isin(bustype_filter)]

    #Route_name
    route_filter = st.sidebar.multiselect("Select Route Names", df_filtered["Route_names"].unique())
    if route_filter:
        df_filtered = df_filtered[df_filtered["Route_names"].isin(route_filter)]

    #Route_link
    route_links_filter = st.sidebar.multiselect("Select Route Links", options=df_filtered["Route_links"].unique().tolist(),default=df_filtered["Route_links"].unique().tolist())
    if route_links_filter:
        df_filtered = df_filtered[df_filtered["Route_links"].isin(route_links_filter)]

    #star_rating
    star_rating_range = st.sidebar.slider("Select Star Rating Range",min_value=0.0,max_value=5.0,value=(0.0, 5.0),step=0.1)
    df_filtered = df_filtered[(df_filtered["Star_rating"] >= star_rating_range[0]) & (df_filtered["Star_rating"] <= star_rating_range[1])]

    #seats
    seats_range = st.sidebar.slider("Select Seats Available Range",min_value=0,max_value=60, value=(0,100),step=1)  
    df_filtered = df_filtered[(df_filtered["Seats_available"] >= seats_range[0]) & (df_filtered["Seats_available"] <= seats_range[1])]

    #price
    price_range = st.sidebar.slider("Select Price Range",min_value=0.0,max_value=5000.0,value=(0.0, 5000.0),step=100.0)
    df_filtered = df_filtered[(df_filtered["Price"] >= price_range[0]) & (df_filtered["Price"] <= price_range[1])]

    # Departing Time
    departing_time_filter = st.sidebar.multiselect("Select Departing Times", options=df_filtered["Departing_time"].unique().tolist(), default=df_filtered["Departing_time"].unique().tolist())
    if departing_time_filter:
        df_filtered = df_filtered[df_filtered["Departing_time"].isin(departing_time_filter)]

    # Reaching Time
    reaching_time_filter = st.sidebar.multiselect("Select Reaching Times",options=df_filtered["Reaching_time"].unique().tolist(),default=df_filtered["Reaching_time"].unique().tolist())
    if reaching_time_filter:
        df_filtered = df_filtered[df_filtered["Reaching_time"].isin(reaching_time_filter)]

    # Duration
    duration_filter = st.sidebar.multiselect("Select Durations",options=df_filtered["Duration"].unique().tolist(),default=df_filtered["Duration"].unique().tolist())
    if duration_filter:
        df_filtered = df_filtered[df_filtered["Duration"].isin(duration_filter)]

    # Bus Name
    busname_filter = st.sidebar.multiselect("Select Bus Names", options=df_filtered["Busname"].unique().tolist(), default=df_filtered["Busname"].unique().tolist())
    if busname_filter:
        df_filtered = df_filtered[df_filtered["Busname"].isin(busname_filter)]

    st.subheader(f"Bus Routes in {state_filter}")
    if df_filtered.empty:
        st.write("No data available for the selected filters.")
    else:
        st.dataframe(df_filtered)

if __name__ == "__main__":
    app()