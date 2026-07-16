import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from yfinance.exceptions import YFRateLimitError
from cleaning import cleanData 
from features import newFeatures
from model import modelTraining
import time
import plotly.graph_objects as go 
import plotly.express as px

stocks = stocks = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META","NVDA", "TSLA", "AMD", "INTC", "ORCL","CRM", "ADBE", "NFLX", "CSCO", "IBM","JPM", "BAC", "WFC", "GS", "MS",
    "AXP", "V", "MA", "BLK", "SCHW","JNJ", "PFE", "MRK", "ABBV", "LLY","UNH", "BMY", "TMO", "AMGN", "CVS","WMT", "COST", "HD", "MCD", "SBUX",
    "NKE", "KO", "PEP", "DIS", "LOW","XOM", "CVX", "COP", "SLB", "EOG","CAT", "BA", "GE", "HON", "UPS","T", "VZ", "TMUS","SPY", "QQQ", "DIA", "VTI", "VOO",
    "AVGO", "QCOM", "TXN", "MU", "ASML","RIVN", "LCID", "NIO", "XPEV"
]
st.markdown("<h1 style = 'text-align: center; margin-bottom: 30px'>Stock Market Analysis And Trend Prediction </h1>", 
    unsafe_allow_html=True)
st.markdown("<h6 style = 'font-size: 20px; text-align: center; margin-bottom:80px;'>Transforming Market Data into Meaningful Insights<br>The Stock Market Analysis & Trend Prediction System is an intelligent analytics platform that combines real-time financial data, advanced technical indicators, interactive visualizations, and machine learning to deliver comprehensive stock market insights. Designed for students, researchers, and investors alike, the platform enables users to explore historical trends, evaluate market behavior, and make data-driven predictions through a seamless and interactive experience</h6>", 
    unsafe_allow_html=True)
    
st.set_page_config(layout="wide", page_title = "Stock Market Analysis and Trend Prediction")
h1, h2 = st.columns([1, 3])

with h1:
    
    st.subheader("STOCK ANALYSIS")
    st.write("Easily compare stocks against each other")
    stocks = st.multiselect("Select stocks for analysing", options=stocks, default= ["AAPL", "MSFT"])
    timeline = st.selectbox("Select the time horizon:", ["10y", "5y", "2y", "1y", "6mo", "3mo", "1mo"])

if stocks:
    data = yf.download(stocks, period=timeline, multi_level_index=False)
    close = data["Close"]
    normalized = close/close.iloc[0] *100
else:
    normalized = [1,1]

with h2:
    st.line_chart(normalized)

st.divider()
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

st.title("Trend Prediction")
stock = st.text_input("Enter the stock for prediction").strip().upper()

if st.button("Predict"):
    
    if (not stock):
        st.warning("Enter a stock symbol to proceed !")
    else:
        df = yf.download(stock, period="10y", interval="1d", multi_level_index=False)

        if df.empty:

            st.error("Please enter a valid stock symbol !")
        elif (len(df)<100):

            st.warning("Not enough stock history availale !")
        else:
            st.session_state.analysis_done = True
            st.session_state.df = df
            st.session_state.stock = stock
        
if st.session_state.analysis_done:
    df = st.session_state.df
    stock = st.session_state.stock
    #Using the Cleaning Function
    df = cleanData(df)
    #Adding new features
    df, last_row = newFeatures(df)
    #Using the RFC model for prediction
    prediction, model, cm, cr, accuracy  = modelTraining(df, last_row)
    c1, c2 = st.columns([1,1])
    with c1:
        st.markdown("<h3 style='margin-top: 120px; display: flex; justify-content: center;'>COMPANY INFORMATION</h3>", unsafe_allow_html=True)

    with c2:
        with st.spinner("Fetching company's information"):
            
            try:
                ticker = yf.Ticker(stock)
                info = ticker.info
                st.subheader(info.get("longName", "Unknown"))
                st.write("Sector: ", info.get("sector", "None"))
                st.write("Industry: ", info.get("industry", "None"))
                st.write("Market Capitalization: ", info.get("marketCap", "None"))
                st.write("Official Website: ", info.get("website", "None"))
                st.write("Exchange: ", info.get("exchange", "None"))
                st.write("Currency: ", info.get("currency", "None"))
            except YFRateLimitError:
                st.info("Yahoo Finance is temporarily limiting company information requests. Please try again later.")
            except Exception:
                st.write("Company information is temporarily unavailable. Please try again later.")
           
    
    st.divider()
    st.subheader("Candle Sticks Analysis")
    cc_check = st.checkbox("Show Bollinger Bands")
    chart = go.Figure(
        data=[
            go.Candlestick(
                x = df.index, 
                open= df["Open"], 
                high= df["High"], 
                low= df["Low"], 
                close= df["Close"],
                increasing_line_color="green",
                decreasing_line_color= "red",
            
            )
        ]
    )
    chart.update_layout(
        xaxis_rangeslider_visible=False,
        # template= "plotly_dark",
        xaxis_range = [df.index[-120], df.index[-1]]
    )
    chart.update_xaxes(
    rangebreaks=[
        dict(bounds=["sat", "mon"])
        ]
    )
    if cc_check:
        chart.add_trace(
            go.Scatter(
                x = df.index,
                y = df["Up_Band"],
                mode = "lines",
                name = "Higher Band"
            )
        )
        chart.add_trace(
            go.Scatter(
                x = df.index,
                y = df["MA_20"],
                mode = "lines",
                name = "Middle Band"
            )
        )
        chart.add_trace(
            go.Scatter(
                x = df.index,
                y = df["Lo_Band"],
                mode = "lines",
                name = "Lower Band"
            )
        )
    st.plotly_chart(chart, width = "stretch")
    
    st.subheader("Volume Bars")
    bar = go.Figure()
    bar.add_trace(go.Bar( x = df.index, y = df["Volume"], name="Volume"))
    bar.update_xaxes(
        range=[df.index[-120], df.index[-1]], 
        rangebreaks = [dict(bounds = ["sat", "mon"])]
        
    )
    st.plotly_chart(bar)

    st.subheader("Stock Data of last 10 years")
    st.write(df)

    c1, c3 = st.columns([1,1])
    with c1:
        
        chart = go.Figure()
        chart.add_trace(
            go.Scatter(
                x = df.index,
                y = df["MA_20"],
                mode = "lines",
                name = "MA_20"
            )
        )
        chart.add_trace(
            go.Scatter(
                x = df.index,
                y = df["MA_50"],
                mode = "lines",
                name = "MA_50"
            )
        )
        chart.add_trace(
            go.Scatter(
                x = df.index,
                y = df["MA_100"],
                mode = "lines",
                name = "MA_100"
            )
        )
        chart.update_xaxes(
            range = [df.index[-200], df.index[-1]]
        )
        st.plotly_chart(chart, width = "stretch")
        st.markdown("<h6 style='margin: 0; padding: 0;text-align: center;'>Moving Averages</h6>", unsafe_allow_html=True)

    

    with c3:
        chart = go.Figure()
        chart.add_trace(
            go.Scatter(
                x = df.index,
                y = df["MACD"],
                mode = "lines",
                name = "MACD"
            )
        )
        chart.add_trace(
            go.Scatter(
                x = df.index,
                y = df["MACD_Signal"],
                mode = "lines",
                name = "Signal"
            )
        )
        chart.add_trace(
            go.Bar(
                x = df.index,
                y = df["Histogram"],
                name = "Histogram"
            )
        )
        chart.update_xaxes(
            range = [df.index[-200], df.index[-1]]
        )
        st.plotly_chart(chart, width = "stretch")
        st.markdown("<h6 style='margin: 0; padding: 0;text-align: center;'>MACD Indicator</h6>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 1])
    with c1:
        chart = go.Figure()
        chart.add_trace(
            go.Scatter(
                x = df.index,
                y = df["D_Return"],
                mode = "lines",
                name = "Daily Returns"
            )
        )
        chart.update_xaxes(
            range = [df.index[-300], df.index[-1]]
        )
        st.plotly_chart(chart, width = "stretch")
        st.markdown("<h6 style='margin: 0; padding: 0;text-align: center;'>Daily Return</h6>", unsafe_allow_html=True)

    with c2:
        chart = go.Figure()
        chart.add_trace(
            go.Heatmap(
                z = cm,
                x = ["Predicted Fall", "Predicted Rise"],
                y = ["Actual Fall", "Actual Rise"],
                text = cm,
                texttemplate = "%{text}",
                textfont = {"size": 18}
            )
        )
        chart.update_yaxes(
            autorange = "reversed"
        )
        st.plotly_chart(chart, width = "stretch")
        st.markdown("<h6 style='margin: 0; margin-bottom: 30px; padding: 0;text-align: center;'>Confusion Matrix</h6>", unsafe_allow_html=True)
    
    st.divider()
    st.subheader("Prediction for tomorrow's Stock")

    c1, c2, c3 = st.columns([1,1,1])
    if prediction:
        pValue = "Rise"
    else:
        pValue = "Fall"
    with c1:
        st.metric(
            "Prediction",
            pValue, 
            border = True
        )
    with c2:
        st.metric(
            "Accuracy",
            f"{accuracy*100:.2f}%", 
            border = True
        )
    with c3:
        st.metric(
            "Volume",
            last_row["Volume"], 
            border = True
        )

    st.info("Hyperparameters were optimized using RandomizedSearchCV with 5-fold cross-validation to obtain the best-performing Random Forest model."
    )

    st.divider()
    st.caption(
    "Prediction is generated using a Random Forest Classifier trained on historical stock market data. "
    "It is intended for educational purposes only and should not be considered financial advice."
    )
    st.caption(f"Last updated: {df.index[-1].date()}")
    st.divider()
    st.markdown("Developed by Gurleen Kaur<br>BCA Final Year Project<br>2026", unsafe_allow_html=True)
    st.divider()