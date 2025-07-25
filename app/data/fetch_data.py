import yfinance as yf
import pandas as pd

def scrape_data(ticker="AAPL", start = "2020-01-01", end = "2024-12-31") -> pd.DataFrame:
    #Create a dataframe that stores data about a specific stock (e.g., AAPL)
    df = yf.download(ticker,start=start,end=end)
    df = df[['Open','High','Low','Close','Volume']] #Columns of dataframe are Open, High, Low, Close, and Volume
    df.dropna(inplace=True) # remove null values
    
    # Don't save to file in Lambda environment (read-only file system)
    # df.to_csv(f"data/{ticker}.csv", index=True)
    
    return df

def load_spy(start = "2020-01-01",end = "2024-12-31"):
    df_spy = yf.download("SPY", start=start, end=end, progress=False)

    # If df_spy["Close"] is already a DataFrame or Series
    spy_series = df_spy["Close"]  # this is a Series

    # Convert to DataFrame properly
    df_spy = pd.DataFrame(spy_series).rename(columns={"Close": "SPY"})

    df_spy["SPY Return"] = df_spy["SPY"].pct_change().fillna(0)
    df_spy["SPY Cumulative"] = (1 + df_spy["SPY Return"]).cumprod()

    return df_spy

if __name__ == "__main__":
    df = scrape_data()
    print(df.head())

