PROJECT_REDBUS:

This repository has a solution for scraping, storing, and visualization of data extraction and analysis of bus route from the Redbus website.The project utilizes Selenium for web scraping, SQL for data storage, and Streamlit for data visualization.The main focus is on gathering details about both government and private bus services, including route information, bus types, pricing, star ratings, and seat availability. The utilization of web scraping techniques and developing an interactive application provides valuable insights and an easy-to-use platform for users to explore and filter bus service data.

Table of Contents:

- Introduction
- Prerequisites
- Skills
- Problem Statement
- Approach
- Project working
- Trouble

Introduction:

This project aims to provide a sturdy solution for collecting, analyzing, and visualizing data from the Red Bus platform. It is divided into three primary components:
 a. Web Scraping Using Selenium: Extracts data from the Red Bus website.
 b. SQL Database creation: Inserts the extracted data into a SQL database.
 c. Streamlit App: Visualizes the data stored in the SQL database.

Prerequisites:

Before running the project,make sure that you have the following installed before starting:
- Python
- Jupyter Notebook/vscode
- Selenium
- Streamlit
- SQL Database (e.g., SQLite, MySQL)

Skills:

- Web Scraping using Selenium
- Python Programming
- Data Visualization with Streamlit
- SQL Database Management

Problem Statement:

The "Redbus Data Scraping and Filtering with Streamlit Application" project focuses on automating the extraction and analysis of bus travel data from the Redbus platform which helps to seeks the revolution for the transportation industry by offering a comprehensive solution for collecting, analyzing, and visualizing bus travel data. Using Selenium for web scraping, the project collects key details such as bus routes, schedules, pricing, and seat availability.By automating data collection, it enhances operational efficiency and supports strategic planning for bus operators and travelers.

Approach:

1.Install Python Libraries:You can install the required Python libraries using pip:
           
pip install selenium mysql-connector-python streamlit

2.Make sure to install ChromeDriver or the appropriate driver for your browser and ensure it matches the version of the browser you are using.The Setup is  

a. Selenium Data Extraction from RedBus: Utilize Selenium to automate the extraction of data from the Redbus website, including routes, schedules, prices, and seat availability.This section demonstrates how to use Selenium to scrape data from the RedBus website.

Step 1: Import necessary libraries

from selenium import webdriver

from selenium.webdriver.common.by import By

import time

import mysql.connector

Step 2: Initialize the WebDriver and navigate to the RedBus website

driver = webdriver.Chrome(executable_path='/path/to/chromedriver')  # Replace with the correct path to your WebDriver

driver.get("https://www.redbus.in/")

time.sleep(5)  # Wait for the page to load

Step 3: Extract data (e.g., bus operators, departure times, prices, etc.)

# Example: Extracting bus operators' names
bus_operators = driver.find_elements(By.XPATH, "//div[@class='button']")

operator_names = [operator.text for operator in bus_operators]

# Example: Extracting bus prices
prices = driver.find_elements((By.XPATH, '//*[@class="fare d-block")]')

for price_elem in price:

    Price.append(price_elem.text) #if you want,you can add additional details like bus timings, seat availability, etc.

Step 4: Close the browser

driver.quit()

3.Store Data in MySQL Database

Step 1: Set up your MySQL database (Create a new database)

# MySQL database
import mysql.connector

connection = mysql.connector.connect(
     
      host="localhost", # Your MySQL server host
      
      user="root",      # Your MySQL username 
      
      password="password")   # Your MySQL password

cursor = connection.cursor()

cursor.execute("create database redbus_data")

print("Database created")

Step 2: Set up a table in the MySQL database 

import mysql.connector

connection = mysql.connector.connect(
 
    host="localhost",   # Your MySQL server host
 
    user="root",        # Your MySQL username

    password="password", # Your MySQL password
 
    database="redbus_data") # Your MySQL database

cursor = connection.cursor()

CREATE TABLE Table_name (id INT AUTO_INCREMENT PRIMARY KEY,operator_name VARCHAR(255),price DECIMAL(10, 2));

print("Table Created successfully")

Step 3: Insert the scraped data into the database

insert_query = ('''INSERT INTO busdetails(Busname,Bustype,Departing_time,Reaching_time,Duration,Price,Seats_Available,Star_rating,Route_links,Route_names)VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''')

data =Final_df.values.tolist() # here Final_df is the cleaned data from scraped data and the cleaned data is converted to a list of lists

try:
   
      cursor.executemany(insert_query, data) # used to insert multiple rows at once
    
      connection.commit()
    
      print("Values inserted successfully")

except Exception as e:
    
      print(f"Error: {e}")

4. Build a Streamlit Application to Join SQL Data and Display

Step 1: Import Streamlit and MySQL libraries

import streamlit as st

import mysql.connector

import pandas as pd

Step 2: Connect to MySQL and fetch data

# Function to create a connection with MySQL database
def fetch_data_from_db():
    
      db_connection = mysql.connector.connect(
         
          host="localhost",      
        
          user="root",
       
          password="password",
        
          database="redbus_data")
    
query = "SELECT * FROM bus_data"
    
df = pd.read_sql(query, db_connection)
    
db_connection.close()
    
return df

Step 3: Create a Streamlit app

# Function to fetch data from the busdetails table

def display_data():
    
    st.title("RedBus Data")

    # Fetch data from the database
    df = fetch_data_from_db()

    # Display data as a table
    st.write(df)

    # Add additional Streamlit components as if needed
    st.bar_chart(df['price'])
    
    st.map(df[['latitude', 'longitude']])

if _name_ == "_main_": # common Python construct that ensures that the code within the app() function is executed 
    
    display_data()   # displays the data

Step 4: Run your Streamlit application

streamlit run app.py

Project Workflow

1. Extract Data from RedBus: Use Selenium to scrape bus operator and pricing data.
2. Store in MySQL: Insert the extracted data into a MySQL database.
3. Display in Streamlit: Fetch the data from MySQL and visualize it using Streamlit.

Troubleshooting

1.Web Scraping Issues: RedBus may update their website structure, causing scraping to break. Check the XPath selectors and update them accordingly.

2.Database Connection Issues: Ensure that MySQL is running and that you have the correct credentials in the connection script.

3.Streamlit Issues: If your Streamlit app doesn’t display data correctly, ensure that your database is populated and that the connection is valid
