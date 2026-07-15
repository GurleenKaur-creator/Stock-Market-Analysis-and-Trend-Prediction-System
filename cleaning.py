import pandas as pd
import numpy as np

def cleanData(df):
 
    #Removing duplicates from the dataframe
    df = df.copy()
    cols = ["Open", "High", "Low", "Close"]
    df = df[~df.index.duplicated(keep = "first")]
    
    #sorting the values using Date
    df = df.sort_index()

    #Removing Impossible values
    for col in df[cols]:
        df.loc[df[col]<=0, col] = np.nan
        df.loc[df[col]>=df[col].mean()*5] = np.nan

    #Finding and fixing missing values
    vals = df[cols].isnull().sum().sum()

    df[cols] = df[cols].ffill()
    df[cols] = df[cols].bfill()

    val = df[cols].isnull().sum().sum()
    

    median = df["Volume"].median()
    df["Volume"] = df["Volume"].fillna(median)

    #High Price and Low Price Rules
    df["High"] = df[cols].max(axis = 1)
    df["Low"] = df[cols].min(axis = 1)

    return df