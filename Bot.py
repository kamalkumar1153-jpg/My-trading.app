import yfinance as yf
import pandas as pd
from datetime import datetime

symbol = "^NSEI" # Nifty 50

def get_prediction():
    data = yf.download(tickers=symbol, period='2d', interval='5m', progress=False)
    if data.empty:
        return "Market is Closed or No Data."

    # Indicators
    data['EMA_9'] = data['Close'].ewm(span=9, adjust=False).mean()
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / (loss + 1e-10) # Avoid division by zero
    data['RSI'] = 100 - (100 / (1 + rs))

    current_price = data['Close'].iloc[-1]
    last_ema = data['EMA_9'].iloc[-1]
    last_rsi = data['RSI'].iloc[-1]
    
    prediction = "SIDEWAYS"
    if current_price > last_ema and last_rsi > 55:
        prediction = "UP (Bullish)"
    elif current_price < last_ema and last_rsi < 45:
        prediction = "DOWN (Bearish)"
    
    return f"Price: {current_price:.2f} | RSI: {last_rsi:.2f} | Prediction: {prediction}"

if __name__ == "__main__":
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {get_prediction()}")
 
    
