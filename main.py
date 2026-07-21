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

df = cleanData(df)
df, last_row  = newFeatures(df)

prediction, cm, accuracy = modelTraining(df, last_row)

if prediction:
    print("Tomorrow's stock price is expected to rise")
else:
    print("Tomorrow's stock price is expected to fall")





