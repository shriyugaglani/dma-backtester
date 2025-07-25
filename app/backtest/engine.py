import pandas as pd
import numpy as np

class BacktestEngine:
    def __init__(self, df):
        self.df = df.copy()
        # self.initial_capital =initial_capital
        self.results = None

    def run_backtest(self,amount, ticker):
        df = self.df.copy()

        # Detect trades: when Position changes (1 = buy, -1 = sell, 0 = hold)
        df['Trade'] = df['Position'].diff().fillna(0)

        cash = amount
        shares = 0
        portfolio_values = []


        for idx, row in df.iterrows():
            price = row[('Close', ticker)]
            trade = row[('Trade', '')]

            # print(type(trade))

            # Buy signal
            if int(trade) == 1:
                shares = cash / price  # buy as many whole shares as possible
                cash -= shares * price

            # Sell signal
            elif int(trade) == -1:
                cash += shares * price
                shares = 0

            portfolio_value = float(cash + shares * price)  # Ensure scalar float
            portfolio_values.append(portfolio_value)

        df['Portfolio Value'] = portfolio_values

        # Calculate returns
        df['Daily Return'] = df['Portfolio Value'].pct_change().fillna(0)
        df['Cumulative Return'] = (1 + df['Daily Return']).cumprod()

        self.results = df
        return df


    def merge_strategy_with_benchmark(self, spy_df):
        """
        Merges strategy cumulative returns with SPY cumulative returns.
        Returns a combined DataFrame for comparison plots.
        """
        combined = self.results.copy()
        spy_df.columns = pd.MultiIndex.from_product([['SPY'], spy_df.columns])
        combined = combined.join(spy_df[[("SPY","SPY Cumulative")]], how="inner")
        combined.rename(columns={"Cumulative Return": "Strategy"}, inplace=True)
        return combined
    
    def final_results(self):
        if self.results is None:
            raise ValueError("Run backtest")
        
        df = self.results.dropna().copy()
        df.index = pd.to_datetime(df.index)

        total_return = df["Cumulative Return"].iloc[-1] - 1

        start = df.index[0]
        end = df.index[-1]
        num_years = (end - start).days / 365.25

        annualized_return = (1 + total_return) ** (1 / num_years) - 1

        cumulative = df["Cumulative Return"].astype(float)
        running_max = cumulative.cummax()
        drawdown = cumulative / running_max - 1
        max_drawdown = drawdown.min()

        sharpe_ratio = (df["Daily Return"].mean() / df["Daily Return"].std()) * np.sqrt(252)

        trades = df[df["Trade"] != 0]
        winning_trades = trades[trades["Daily Return"] > 0]
        win_rate = len(winning_trades) / len(trades) if len(trades) > 0 else 0
        num_trades = df["Trade"].abs().sum()

        return {
            "Total Return": f"{total_return:.2%}",
            "Annualized Return": f"{annualized_return:.2%}",
            "Max Drawdown": f"{max_drawdown:.2%}",
            "Sharpe Ratio": f"{sharpe_ratio:.2f}",
            "Win Rate": f"{win_rate:.2%}",
            "Number of Trades": int(num_trades),
            "Start Date": start.strftime("%Y-%m-%d"),
            "End Date": end.strftime("%Y-%m-%d"),
            "Years": f"{num_years:.2f}"
        }