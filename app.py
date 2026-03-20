import yfinance as yf
import pandas as pd
from flask import Flask, render_template, jsonify
import threading
import time

app = Flask(__name__)

# Dono market ka data store karne ke liye dictionary
market_signals = {
    "NIFTY": {"price": "0", "rsi": "0", "signal": "Wait", "color": "white"},
    "SENSEX": {"price": "0", "rsi": "0", "signal": "Wait", "color": "white"}
}

def get_signal(symbol):
    try:
        data = yf.download(tickers=symbol, period='1d', interval='5m', progress=False)
        if data.empty: return {"price": "N/A", "rsi": "0", "signal": "Closed", "color": "gray"}

        # Indicators
        data['EMA_9'] = data['Close'].ewm(span=9, adjust=False).mean()
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / (loss + 1e-10)
        rsi = 100 - (100 / (1 + rs))

        curr_p = data['Close'].iloc[-1]
        last_rsi = rsi.iloc[-1]
        last_ema = data['EMA_9'].iloc[-1]

        # Logic
        if curr_p > last_ema and last_rsi > 55:
            return {"price": f"{curr_p:.2f}", "rsi": f"{last_rsi:.1f}", "signal": "UP", "color": "#00ff88"}
        elif curr_p < last_ema and last_rsi < 45:
            return {"price": f"{curr_p:.2f}", "rsi": f"{last_rsi:.1f}", "signal": "DOWN", "color": "#ff4444"}
        else:
            return {"price": f"{curr_p:.2f}", "rsi": f"{last_rsi:.1f}", "signal": "SIDEWAYS", "color": "#aaaaaa"}
    except:
        return {"price": "Error", "rsi": "0", "signal": "Error", "color": "white"}

def update_loop():
    global market_signals
    while True:
        market_signals["NIFTY"] = get_signal("^NSEI")
        market_signals["SENSEX"] = get_signal("^BSESN")
        time.sleep(300) # 5 Minute wait

threading.Thread(target=update_loop, daemon=True).start()

@app.route('/')
def index(): return render_template('index.html')

@app.route('/api/data')
def data(): return jsonify(market_signals)

if __name__ == "__main__":
    app.run(port=8000)
    
 
    
