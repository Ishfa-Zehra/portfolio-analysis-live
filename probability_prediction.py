import sqlite3
import pandas as pd
import numpy as np

def probability_based_prediction():
    conn = sqlite3.connect('portfolio_database.db')

    try:
        df = pd.read_sql_query("SELECT * FROM Portfolio_Returns ORDER BY Date", conn)
        df['Date'] = pd.to_datetime(df['Date'])

        mean_return = df['Portfolio_Return'].mean()
        std_return  = df['Portfolio_Return'].std()

        # METHOD 1: Simple Moving Average (SMA)
        df['SMA_5']  = df['Portfolio_Return'].rolling(window=5).mean()
        sma_prediction = df['Portfolio_Return'].tail(5).mean()

        # METHOD 2: Exponential Moving Average (EMA)
        df['EMA_10'] = df['Portfolio_Return'].ewm(span=10, adjust=False).mean()
        ema_prediction = df['EMA_10'].iloc[-1]

        # METHOD 3: Probability of positive return
        prob_positive = (df['Portfolio_Return'] > 0).sum() / len(df)

        # METHOD 4: Confidence intervals
        ci_lower_95 = mean_return - 1.96 * std_return
        ci_upper_95 = mean_return + 1.96 * std_return
        ci_lower_68 = mean_return - std_return
        ci_upper_68 = mean_return + std_return

        # METHOD 5: Conditional probability based on today's return
        today_return  = df['Portfolio_Return'].iloc[-1]
        similar_days  = df[abs(df['Portfolio_Return'] - today_return) < 0.5]
        next_returns  = [df.iloc[i+1]['Portfolio_Return'] for i in similar_days.index if i+1 < len(df)]
        prob_up_after = sum(1 for r in next_returns if r > 0) / len(next_returns) if next_returns else 0.5

        # Print summary
        print(f"SMA-5  Prediction : {sma_prediction:.4f}%")
        print(f"EMA-10 Prediction : {ema_prediction:.4f}%")
        print(f"P(Positive Return): {prob_positive:.2%}")
        print(f"68% CI : [{ci_lower_68:.2f}%, {ci_upper_68:.2f}%]")
        print(f"95% CI : [{ci_lower_95:.2f}%, {ci_upper_95:.2f}%]")
        print(f"P(Up tomorrow | today={today_return:.2f}%): {prob_up_after:.2%}")

        # Save to database
        predictions_df = df[['Date','Portfolio_Return','SMA_5','EMA_10']].dropna()
        predictions_df.columns = ['Date','Actual_Return','SMA_5_Prediction','EMA_10_Prediction']
        predictions_df.to_sql('Probability_Predictions', conn, if_exists='replace', index=False)

        summary_df = pd.DataFrame({
            'Metric': ['SMA_Prediction','EMA_Prediction','Prob_Positive',
                       'CI_68_Lower','CI_68_Upper','CI_95_Lower','CI_95_Upper'],
            'Value' : [sma_prediction, ema_prediction, prob_positive,
                       ci_lower_68, ci_upper_68, ci_lower_95, ci_upper_95]
        })
        summary_df.to_sql('Probability_Summary', conn, if_exists='replace', index=False)
        print("Results saved to database.")

    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    probability_based_prediction()