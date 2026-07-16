# 📈 Stock Market Analysis and Trend Prediction

A Machine Learning-based application that analyzes historical stock market data, visualizes market trends through interactive charts, and predicts the **next trading day's stock movement** using a **Random Forest Classifier**.

Developed as a **Bachelor of Computer Applications (BCA) Final Year Project**.

#Features

- 📊 Interactive Candlestick Chart
- 📈 Moving Average Analysis (5, 20, 50, 100 & 200 Days)
- 📉 MACD Indicator
- 📌 Bollinger Bands
- 📊 Daily Return Visualization
- 📈 Rolling Volatility Analysis
- 🏢 Company Information Retrieval
- 🤖 Next-Day Stock Trend Prediction
- 📋 Confusion Matrix
- 📄 Classification Report
- ⚡ Input Validation & Error Handling
- 🎨 Interactive Streamlit Dashboard

---

#Technologies Used

| Category | Technology |
|----------|------------|
| Language | Python |
| Web Framework | Streamlit |
| Data Analysis | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Data Source | Yahoo Finance (yfinance) |
| Visualization | Plotly |
| Technical Indicators | TA Library |

---

#Project Structure

```text
Stock-Market-Analysis/
│
├── app.py                 # Streamlit Web Application
├── main.py                # Terminal-Based Application
├── cleaning.py            # Data Cleaning & Preprocessing
├── features.py            # Feature Engineering
├── model.py               # Machine Learning Model
├── requirements.txt       # Project Dependencies
└── README.md
```

---

#Machine Learning Workflow

1. Download historical stock data using Yahoo Finance.
2. Clean and preprocess the dataset.
3. Generate technical indicators and lag features.
4. Train a Random Forest Classifier.
5. Evaluate the model using multiple performance metrics.
6. Predict the next trading day's market direction.
7. Display interactive visualizations and prediction results.

---

#Technical Indicators Used

- Simple Moving Averages (5, 20, 50, 100 & 200)
- Relative Strength Index (RSI)
- MACD
- MACD Signal Line
- MACD Histogram
- Bollinger Bands
- Daily Percentage Return
- Rolling Volatility
- Previous Closing Price (Lag Features)

---

#Model Evaluation

The model is evaluated using:

- Accuracy Score
- Confusion Matrix
- Classification Report
- Precision
- Recall
- F1-Score

---

#Installation

## Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

## Navigate to the project folder

```bash
cd YOUR_REPOSITORY
```

## Install the required libraries

```bash
pip install -r requirements.txt
```

---

#Running the Project

## Streamlit Web Application

```bash
streamlit run app.py OR python -m streamlit run app.py
```

## Terminal-Based Application

```bash
python main.py
```

# ⚠️ Disclaimer

This project is intended **solely for educational and academic purposes**.

Stock market predictions are generated using historical market data and machine learning techniques. They **should not be considered financial or investment advice**.

---

# 👩‍💻 Author

**Gurleen Kaur**

Bachelor of Computer Applications (BCA)

Final Year Project • 2026

---

## ⭐ If you found this project useful, consider giving it a star on GitHub!