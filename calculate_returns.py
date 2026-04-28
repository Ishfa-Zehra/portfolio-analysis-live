import sqlite3
import pandas as pd

def calculate_portfolio_returns():
    conn = sqlite3.connect('portfolio_database.db')
    try:
        query = """SELECT Date, Stock_Name, Closing_Price
                   FROM Stock_Prices WHERE Stock_Name = 'AAPL' ORDER BY Date ASC"""
        price_data = pd.read_sql_query(query, conn)
        price_data['Date'] = pd.to_datetime(price_data['Date'])

        price_data['Daily_Return'] = price_data['Closing_Price'].pct_change() * 100
        price_data = price_data.dropna()

        portfolio_returns = price_data[['Date', 'Daily_Return']].copy()
        portfolio_returns.columns = ['Date', 'Portfolio_Return']
        portfolio_returns['Date'] = portfolio_returns['Date'].dt.strftime('%Y-%m-%d')

        portfolio_returns.to_sql('Portfolio_Returns', conn, if_exists='replace', index=False)

        print(f"Records processed : {len(portfolio_returns)}")
        print(f"Mean daily return : {portfolio_returns['Portfolio_Return'].mean():.4f}%")
        print(f"Volatility (std)  : {portfolio_returns['Portfolio_Return'].std():.4f}%")
        print(f"Min / Max return  : {portfolio_returns['Portfolio_Return'].min():.4f}% / {portfolio_returns['Portfolio_Return'].max():.4f}%")

    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    calculate_portfolio_returns()