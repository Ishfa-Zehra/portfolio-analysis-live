import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def fmt(ax, title, xlabel, ylabel):
    ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

def create_clean_dashboard():
    conn = sqlite3.connect('portfolio_database.db')
    try:
        stocks    = pd.read_sql_query("SELECT * FROM Stock_Prices", conn)
        exchange  = pd.read_sql_query("SELECT * FROM Exchange_Rates", conn)
        portfolio = pd.read_sql_query("SELECT * FROM Portfolio_Returns", conn)
        preds     = pd.read_sql_query("SELECT * FROM Probability_Predictions", conn)
        risk      = pd.read_sql_query("SELECT * FROM Risk_Metrics", conn)
        for df in [stocks, exchange, portfolio, preds]:
            df['Date'] = pd.to_datetime(df['Date'])

        fig = plt.figure(figsize=(20, 12))
        fig.suptitle('Portfolio Risk Analysis Dashboard', fontsize=20, fontweight='bold', y=0.98)
        gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.25, top=0.93, bottom=0.08, left=0.05, right=0.95)

        ax1 = fig.add_subplot(gs[0, 0])
        aapl = stocks[stocks['Stock_Name'] == 'AAPL']
        ax1.plot(aapl['Date'], aapl['Closing_Price'], color='#1f77b4', linewidth=1.5)
        fmt(ax1, 'Apple Stock Price (AAPL)', 'Date', 'Price (USD)')

        ax2 = fig.add_subplot(gs[0, 1])
        ax2.plot(exchange['Date'], exchange['Exchange_Rate'], color='#2ca02c', linewidth=1.5)
        fmt(ax2, 'EUR/USD Exchange Rate', 'Date', 'Rate')

        ax3 = fig.add_subplot(gs[0, 2])
        mean_r = portfolio['Portfolio_Return'].mean()
        ax3.hist(portfolio['Portfolio_Return'], bins=40, color='#9467bd', alpha=0.7, edgecolor='black', linewidth=0.5)
        ax3.axvline(mean_r, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_r:.2f}%')
        ax3.set_title('Returns Distribution', fontsize=12, fontweight='bold', pad=10)
        ax3.set_xlabel('Daily Return (%)', fontsize=10)
        ax3.set_ylabel('Frequency', fontsize=10)
        ax3.legend(fontsize=9)
        ax3.grid(True, alpha=0.3, axis='y', linestyle='--')

        ax4 = fig.add_subplot(gs[1, 0])
        ax4.plot(portfolio['Date'], portfolio['Portfolio_Return'], color='#1f77b4', alpha=0.6, linewidth=0.8)
        ax4.axhline(y=0, color='red', linestyle='--', alpha=0.5, linewidth=1)
        fmt(ax4, 'Portfolio Daily Returns', 'Date', 'Return (%)')

        ax5 = fig.add_subplot(gs[1, 1])
        idx = range(0, len(preds), 10)
        ax5.plot(preds['Date'].iloc[idx], preds['Actual_Return'].iloc[idx], label='Actual', color='#1f77b4', linewidth=1)
        ax5.plot(preds['Date'].iloc[idx], preds['SMA_5_Prediction'].iloc[idx], label='Predicted', color='#d62728', linewidth=1)
        ax5.legend(fontsize=9)
        fmt(ax5, 'Actual vs Predicted Returns', 'Date', 'Return (%)')

        ax6 = fig.add_subplot(gs[1, 2])
        ax6.axis('off')
        rd = dict(zip(risk['Metric'], risk['Value']))
        text = '\n'.join([
            'Risk Metrics Summary', '',
            f"Overall Volatility:\n  {rd.get('Overall_Volatility',0):.4f}%", '',
            f"High FX Volatility:\n  {rd.get('High_Exchange_Volatility',0):.4f}%", '',
            f"Low FX Volatility:\n  {rd.get('Low_Exchange_Volatility',0):.4f}%", '',
            f"Correlation:\n  {rd.get('Correlation',0):.4f}"
        ])
        ax6.text(0.5, 0.5, text, transform=ax6.transAxes, fontsize=11,
                 va='center', ha='center', family='monospace',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))

        plt.savefig('portfolio_dashboard.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.show()
        print("Dashboard saved: portfolio_dashboard.png")
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    create_clean_dashboard()