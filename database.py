import sqlite3
import pandas as pd

conn   = sqlite3.connect('portfolio_database.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Stock_Prices (
    Date TEXT, Stock_Name TEXT, Closing_Price REAL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Exchange_Rates (
    Date TEXT, Currency_Pair TEXT, Exchange_Rate REAL)''')

apple_df = pd.read_csv('apple_stock_data.csv')
apple_df['Date']       = apple_df['Date'].str.split(' ').str[0]
apple_df['Stock_Name'] = 'AAPL'
apple_df               = apple_df[['Date', 'Stock_Name', 'Close']]
apple_df.columns       = ['Date', 'Stock_Name', 'Closing_Price']
apple_df.to_sql('Stock_Prices', conn, if_exists='replace', index=False)
print(f"Added {len(apple_df)} Apple stock records")

exchange_df = pd.read_csv('exchange_rate_data.csv')
exchange_df['Date']          = exchange_df['Date'].str.split(' ').str[0]
exchange_df['Currency_Pair'] = 'EUR/USD'
exchange_df                  = exchange_df[['Date', 'Currency_Pair', 'Close']]
exchange_df.columns          = ['Date', 'Currency_Pair', 'Exchange_Rate']
exchange_df.to_sql('Exchange_Rates', conn, if_exists='replace', index=False)
print(f"Added {len(exchange_df)} exchange rate records")

cursor.execute("SELECT COUNT(*) FROM Stock_Prices")
print(f"Stock prices in DB   : {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM Exchange_Rates")
print(f"Exchange rates in DB : {cursor.fetchone()[0]}")

conn.close()