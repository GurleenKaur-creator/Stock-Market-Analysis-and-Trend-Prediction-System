import pandas as pd
import numpy as np
import yfinance as yf
import sys
from cleaning import cleanData 
from features import newFeatures
from model import modelTraining

con = True
while con:
    stock = input("Enter the stock for prediction: ").strip().upper()
    if (stock == ""):
        print("Kindly enter a valid stock symbol!")
    else:
        con = False

data = yf.Ticker(stock)
df = data.history(period="10y")


if (df.empty):
    print("This stock does not exist !")
    sys.exit()

elif (len(df)<100):
    print("Not enough stock history available !")
    sys.exit()

else:
    print("..........PROCEEDING..........")

# print(df.head())

df = cleanData(df)
df, last_row  = newFeatures(df)
prediction, model, cm, cr, accuracy = modelTraining(df, last_row)
# print(f"All columns are:  \n{df.columns.to_list()}")
# print(df["Target"].value_counts(normalize=True) * 100)
# print(cm)
# print(cr)
# print(prob.min())
# print(prob.max())
# print(prob.mean())
# print(ut_values, up_values)
if prediction:
    print("Tomorrow's stock price is expected to rise")
else:
    print("Tomorrow's stock price is expected to fall")





