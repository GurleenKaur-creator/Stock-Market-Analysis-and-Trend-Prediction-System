import numpy as np
import pandas as pd
import ta

def newFeatures(df):

    #Removing unused columns
    #df = df.drop(columns = [ "Dividends", "Stock Splits"])

    #Daily's Price Change
    df["P_Change"] = df["Close"]-df["Open"]

    #Daily Range: Price movement during the day
    df["D_Range"] = df["High"]-df["Low"]

    #Daily Return, 5 and 10 day return
    df["D_Return"] = df["Close"].pct_change()
    df["5d_Return"] = df["Close"].pct_change(5)
    df["10d_Return"] = df["Close"].pct_change(10)

    #Volatility
    df["Volatility"] = df["D_Return"].rolling(20).std()

    #Moving Average of 20 days
    df["MA_20"] = df["Close"].rolling(20).mean()

    #Moving Average of 50 days
    df["MA_50"] = df["Close"].rolling(50).mean()

    #Moving Average of 100 days
    df["MA_100"] = df["Close"].rolling(100).mean()

    #RSI: Relative Strength Index
    df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()

    #Close values of previous days
    df["Close_1"] = df["Close"].shift(1)
    df["Close_2"] = df["Close"].shift(2)
    df["Close_3"] = df["Close"].shift(3)
    df["Close_5"] = df["Close"].shift(5)
    
    df["HL_%"] = ((df["High"] - df["Low"]) / df["Close"]) * 100
    df["OC_%"] = ((df["Close"] - df["Open"]) / df["Open"]) * 100

    #Volume value of precvious day
    df["Volume_1"] = df["Volume"].shift(1)

    #EMA: Exponential Moving Average
    df["EMA_12"] = df["Close"].ewm(span=12, adjust=False).mean()
    df["EMA_26"] = df["Close"].ewm(span=26, adjust=False).mean()

    #MACD: Moving Average Convergence Divergence, Signal and Hostogram
    macd = ta.trend.MACD(df["Close"])
    df["MACD"] = macd.macd()
    df["MACD_Signal"] = macd.macd_signal()
    df["Histogram"] = macd.macd_diff()

    #Bollinger Bands
    std = df["Close"].rolling(20).std()
    df["Up_Band"] = df["MA_20"]+ (2*std)
    df["Lo_Band"] = df["MA_20"]- (2*std)

    #Bollinger Bands Width
    df["BB_Width"] = df["Up_Band"] - df["Lo_Band"]

    #A target column
    df["Next_Day"] = df["Close"].shift(-1)
    
    mask = df["Next_Day"]>df["Close"]
    df["Target"] = mask.astype(int)

    #Storing Last row and removing it from the dataframe
    last_row = df.iloc[[-1]]
    df = df.iloc[:-1]
    last_row = last_row.drop(columns=["Target", "Next_Day", "Up_Band", "Lo_Band"], errors = "ignore")

    df = df.dropna().copy()

    return df, last_row