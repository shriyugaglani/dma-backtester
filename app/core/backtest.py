from backtest.engine import BacktestEngine
from data.fetch_data import scrape_data
from strategies.sma_crossover import generate_signal
from models.schemas import BacktestSummary
import pandas as pd
from fastapi import HTTPException

def run_full_backtest(ticker:str, start:str, end:str,amount:int):
    try:
        df = scrape_data(ticker, start, end)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Data fetch failed for {ticker}: {str(e)}")
    
    df = generate_signal(df)
    engine = BacktestEngine(df)
    results = engine.run_backtest(amount, ticker)
    stats = engine.final_results()
    results.copy()
    results.reset_index(inplace=True)

    results["Date"] = pd.to_datetime(results["Date"])
    results["Year"] = results["Date"].dt.year
    yearly_return = (
        results.groupby("Year")["Cumulative Return"]
        .apply(lambda x: (x.iloc[-1] / x.iloc[0]) - 1)
        .reset_index()
        .rename(columns={"Cumulative Return": "Yearly Return"})
    )
    yearly_return_dict = yearly_return.set_index("Year")["Yearly Return"].to_dict()

    return results[["Date", "Portfolio Value", "Cumulative Return"]],BacktestSummary(
        total_return=stats["Total Return"],
        annualized_return=stats["Annualized Return"],
        max_drawdown=stats["Max Drawdown"],
        sharpe_ratio=stats["Sharpe Ratio"],
        win_rate=stats["Win Rate"],
        num_trades=stats["Number of Trades"],
        start_date=stats["Start Date"],
        end_date=stats["End Date"],
        years=stats["Years"]
    ), yearly_return_dict