import sqlite3
import pandas as pd
import numpy as np

def analyze_portfolio_risk():
    conn = sqlite3.connect('portfolio_database.db')
    try:
        portfolio_df = pd.read_sql_query("SELECT Date, Portfolio_Return FROM Portfolio_Returns ORDER BY Date", conn)
        exchange_df  = pd.read_sql_query("SELECT Date, Exchange_Rate FROM Exchange_Rates ORDER BY Date", conn)

        portfolio_df['Date'] = pd.to_datetime(portfolio_df['Date'])
        exchange_df['Date']  = pd.to_datetime(exchange_df['Date'])

        merged = pd.merge(portfolio_df, exchange_df, on='Date', how='inner')
        merged['Exchange_Change']     = merged['Exchange_Rate'].pct_change() * 100
        merged['Exchange_Change_Abs'] = merged['Exchange_Change'].abs()
        merged = merged.dropna()

        overall_volatility = merged['Portfolio_Return'].std()
        threshold          = merged['Exchange_Change_Abs'].quantile(0.75)
        high_vol           = merged[merged['Exchange_Change_Abs'] >  threshold]['Portfolio_Return'].std()
        low_vol            = merged[merged['Exchange_Change_Abs'] <= threshold]['Portfolio_Return'].std()
        correlation        = merged['Portfolio_Return'].corr(merged['Exchange_Change'])

        risk_metrics = pd.DataFrame({
            'Metric': ['Overall_Volatility','High_Exchange_Volatility','Low_Exchange_Volatility','Correlation','Threshold'],
            'Value' : [overall_volatility, high_vol, low_vol, correlation, threshold]
        })
        risk_metrics.to_sql('Risk_Metrics', conn, if_exists='replace', index=False)

        print(f"Overall volatility       : {overall_volatility:.4f}%")
        print(f"High FX change volatility: {high_vol:.4f}%")
        print(f"Low FX change volatility : {low_vol:.4f}%")
        print(f"Correlation (FX vs ret)  : {correlation:.4f}")

    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    analyze_portfolio_risk()