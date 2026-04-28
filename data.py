import yfinance as yf

apple = yf.Ticker("AAPL")
data  = apple.history(start="2022-01-01", end="2026-02-24")

print(f"Downloaded {len(data)} days of Apple stock data")
print(data.head())
print(data.tail())

data.to_csv('apple_stock_data.csv')
print("Saved to: apple_stock_data.csv")