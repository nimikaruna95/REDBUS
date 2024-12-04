import streamlit as st
import mysql.connector
import pandas as pd

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
            database="REDBUS"
        )
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

def fetch_data(state_name_filter, busname_filter, bustype_filter, route_link_filter, route_name_filter, departing_time_filter, reaching_time_filter, duration_filter, price_min, price_max, seats_min, seats_max):
    connection = create_connection()
    if not connection:
        return []
    
    cursor = connection.cursor(dictionary=True)  
    query = "SELECT * FROM busdetails"
    
    filters = []
    params = []

    if state_name_filter:
        filters.append("state_name = %s")
        params.append(state_name_filter)
 
    if busname_filter:
        filters.append("Busname LIKE %s")
        params.append(f"%{busname_filter}%")
    
    if bustype_filter:
        filters.append("Bustype LIKE %s")
        params.append(f"%{bustype_filter}%")
    
    if route_link_filter:
        filters.append("Route_links LIKE %s")
        params.append(f"%{route_link_filter}%")
    
    if route_name_filter:
        filters.append("Route_names LIKE %s")
        params.append(f"%{route_name_filter}%")
    
    if departing_time_filter:
        filters.append("Departing_time >= %s")
        params.append(departing_time_filter)
    
    if reaching_time_filter:
        filters.append("Reaching_time <= %s")
        params.append(reaching_time_filter)
    
    if duration_filter:
        filters.append("Duration <= %s")
        params.append(duration_filter)
    
    if price_min is not None:
        filters.append("Price >= %s")
        params.append(price_min)
    
    if price_max is not None:
        filters.append("Price <= %s")
        params.append(price_max)
    
    if seats_min is not None:
        filters.append("Seats_available >= %s")
        params.append(seats_min)
    
    if seats_max is not None:
        filters.append("Seats_available <= %s")
        params.append(seats_max)
      
    if filters:
        query += " WHERE " + " AND ".join(filters)
    
    try:
        cursor.execute(query, tuple(params))  
        result = cursor.fetchall()  
    except mysql.connector.Error as err:
        st.error(f"Error fetching data: {err}")
        result = []
    
    connection.close()
    return result

def fetch_busnames():
    connection = create_connection()
    if not connection:
        return []
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT DISTINCT Busname FROM busdetails")  
    busnames = cursor.fetchall()
    connection.close()
    return [bus['Busname'] for bus in busnames]

def fetch_bustypes():
    connection = create_connection()
    if not connection:
        return []
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT DISTINCT Bustype FROM busdetails")  
    bustypes = cursor.fetchall()
    connection.close()
    return [bus['Bustype'] for bus in bustypes]

def fetch_route_links():
    connection = create_connection()
    if not connection:
        return []
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT DISTINCT Route_links FROM busdetails")  
    route_links = cursor.fetchall()
    connection.close()
    return [route['Route_links'] for route in route_links]

def fetch_route_names():
    connection = create_connection()
    if not connection:
        return []
    
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT DISTINCT Route_names FROM busdetails")  
    route_names = cursor.fetchall()
    connection.close()
    return [route['Route_names'] for route in route_names]

def fetch_departing_time():
    connection = create_connection()
    if not connection:
        return []
    
    cursor=connection.cursor(dictionary=True)
    cursor.execute("SELECT DISTINCT Departing_time FROM busdetails")
    departing_time = cursor.fetchall()
    connection.close()
    return [time['Departing_time'] for time in departing_time]

def fetch_reaching_time():
    connection = create_connection()
    if not connection:
        return []

    cursor=connection.cursor(dictionary=True)
    cursor.execute("SELECT DISTINCT Reaching_time FROM busdetails")
    reaching_time = cursor.fetchall()
    connection.close()
    return [time['Reaching_time'] for time in reaching_time]

def fetch_duration():
    connection = create_connection()
    if not connection:
        return []

    cursor=connection.cursor(dictionary=True)
    cursor.execute("SELECT DISTINCT Duration FROM busdetails")
    duration = cursor.fetchall()
    connection.close()
    return [time['Duration'] for time in duration]

def app():
    st.title('Database Data View')
    
    # Fetch busnames, bustypes, route_links, and route_names for filters
    busnames = fetch_busnames()
    bustypes = fetch_bustypes()
    route_links = fetch_route_links()
    route_names = fetch_route_names()
    departing_time = fetch_departing_time()
    reaching_time = fetch_reaching_time()
    duration = fetch_duration()

    if not busnames or not bustypes or not route_links or not route_names or not departing_time or not reaching_time or not duration:
        st.error("Could not fetch required data from the database.")
        return

    # Create filter options for user
    state_name_filter = st.text_input('Enter State Name')
    busname_filter = st.selectbox('Select a Busname', [''] + busnames)
    bustype_filter = st.selectbox('Select a Bustype', [''] + bustypes)
    route_link_filter = st.selectbox('Select a Route Link', [''] + route_links)
    route_name_filter = st.selectbox('Select a Route Name', [''] + route_names)
    
    # Add time input filters for departing time and reaching time
    departing_time_filter = st.selectbox('Departing Time',['']+departing_time)
    reaching_time_filter = st.selectbox('Reaching Time',['']+reaching_time)
    duration_filter = st.selectbox('Duration',['']+duration)
    
    # Add number input filters for duration, price, and seat availability
    duration_filter = st.number_input('Max Duration (in hours)', min_value=0, value=0)
    price_min = st.number_input('Min Price', min_value=0, value=0)
    price_max = st.number_input('Max Price', min_value=0, value=1000)
    seats_min = st.number_input('Min Seats Available', min_value=0, value=0)
    seats_max = st.number_input('Max Seats Available', min_value=0, value=50)  

    st.write('Fetching data from MySQL database...')

    # Corrected function call to include the new filters
    data = fetch_data(state_name_filter, busname_filter, bustype_filter, route_link_filter, route_name_filter, departing_time_filter, reaching_time_filter, duration_filter, price_min, price_max, seats_min, seats_max)

    df = pd.DataFrame(data)

    if not df.empty:
        st.write(df)
    else:
        st.write("No data found.")

if __name__ == "__main__":
    app()

