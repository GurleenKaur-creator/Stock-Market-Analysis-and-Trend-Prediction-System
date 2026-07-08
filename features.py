import numpy as np
import pandas as pd
import ta

def newFeatures(df):

    print("..........CREATING NEW FEATURES FOR TECHNICAL ANALYSIS..........")

    #Daily's Price Change
    df["P_Change"] = df["Close"]-df["Open"]

    #Daily Range: Price movement during the day
    df["D_Range"] = df["High"]-df["Low"]

    #Moving Average of 5 days
    df["MA_5"] = df["Close"].rolling(5).mean()

    #Moving Average of 20 days
    df["MA_20"] = df["Close"].rolling(20).mean()

    #RSI: Relative Strength Index
    df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()

    #Close values of previous days
    df["Close_1"] = df["Close"].shift(1)
    df["Close_2"] = df["Close"].shift(2)
    df["Close_3"] = df["Close"].shift(3)

    #MACD: Moving Average Convergence Divergence, Signal and Hostogram
    macd = ta.trend.MACD(df["Close"])
    df["MACD"] = macd.macd()
    df["MACD_Signal"] = macd.macd_signal()
    df["Histogram"] = macd.macd_diff()

    #A target column
    df["Next_Day"] = df["Close"].shift(-1)
    
    mask = df["Next_Day"]>df["Close"]
    df["Target"] = mask.astype(int)

    #Storing Last row and removing it from the dataframe
    last_row = df.iloc[[-1]]
    df = df.iloc[:-1]
    last_row = last_row.drop(columns=["Target", "Next_Day", "Dividends", "Stock Splits"])

    #printing column names
    print("...................")
    print("...New Features Created...")
    # print(f"All columns are:  \n{df.columns.to_list()}")

    df = df.dropna().copy()

    return df, last_row