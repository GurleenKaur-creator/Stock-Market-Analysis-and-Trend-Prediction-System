import pandas as pd
import numpy as np

def cleanData(df):
 
    #Removing duplicates from the dataframe
    df = df.copy()
    cols = ["Open", "High", "Low", "Close"]
    print(f"Length of data before removing duplicates: {len(df)}")
    df = df[~df.index.duplicated(keep = "first")]
    print(f"Length of data after removing duplicates: {len(df)}")
    print(f"......Removed Duplicates...... ")


    #sorting the values using Date
    df = df.sort_index()
    print(f"......Sorted the values using Date...... ")


    #Removing Impossible values
    for col in df[cols]:
        df.loc[df[col]<=0, col] = np.nan
        df.loc[df[col]>=df[col].mean()*5] = np.nan



    #Finding and fixing missing values
    vals = df[cols].isnull().sum().sum()
    print(f"Number of missing values in the data before fixing are: {vals}")


    df[cols] = df[cols].ffill()
    df[cols] = df[cols].bfill()
    

    val = df[cols].isnull().sum().sum()
    print(f"Number of missing values in the data after fixing are: {val}")
    

    median = df["Volume"].median()
    df["Volume"] = df["Volume"].fillna(median)
    print("..........Fixed Missing Values..........")


    #High Price and Low Price Rules
    df["High"] = df[cols].max(axis = 1)
    df["Low"] = df[cols].min(axis = 1)

    return df