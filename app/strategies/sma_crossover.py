import pandas as pd
import numpy as np

def generate_signal(df, short_window=20, long_window=50):
    df = df.copy()

    # Calculate moving averages
    df["SMA Short"] = df["Close"].rolling(window=short_window).mean()
    df["SMA Long"] = df["Close"].rolling(window=long_window).mean()

    # Generate Signal: 1 if SMA Short > SMA Long, else 0
    df["Signal"] = 0
    df.loc[df["SMA Short"] > df["SMA Long"], "Signal"] = 1

    # Position is the previous day's signal (shifted)
    df["Position"] = df["Signal"].shift(1).fillna(0)
    df["Position"] = df["Position"].astype(int)

    return df