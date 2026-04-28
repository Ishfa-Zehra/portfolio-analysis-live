import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# 1. The Heading - Like a poster for your project
st.set_page_config(page_title="Stock Analysis", page_icon="📈")
st.title("Apple Stock & Risk Analysis")
st.write("A professional project for NED University")

# 2. Open the Database - This is where your data is hidden
conn = sqlite3.connect('portfolio_database.db')

# 3. Create a Sidebar - This makes it look very professional
st.sidebar.header("Project Info")
st.sidebar.write("Created by: Ishfa Zehra / Niwas Panwar")
st.sidebar.write("Subject: Programming Language")

# 4. Show the Stock Table
st.subheader("Recent Stock Data")
# We ask the database for the 5 newest rows
df_stocks = pd.read_sql_query("SELECT * FROM Stock_Prices ORDER BY Date DESC LIMIT 5", conn)
st.dataframe(df_stocks)

# 5. Show the Magic Graph
st.subheader("Price Movement over Time")
chart_data = pd.read_sql_query("SELECT Date, Closing_Price FROM Stock_Prices", conn)
chart_data['Date'] = pd.to_datetime(chart_data['Date'])

fig, ax = plt.subplots()
ax.plot(chart_data['Date'], chart_data['Closing_Price'], color='#1f77b4')
plt.xticks(rotation=45)
ax.set_ylabel("Price ($)")
st.pyplot(fig)

# 6. Show Risk Results (from your risk_analysis.py work)
st.subheader("Risk Insights")
try:
    risk_df = pd.read_sql_query("SELECT * FROM Risk_Metrics", conn)
    st.write("How much the stock 'wiggles' (Volatility):")
    st.table(risk_df)
except:
    st.write("Run your analysis scripts to see risk metrics here!")

conn.close()