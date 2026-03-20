import yfinance as yf
import pandas as pd
from datetime import datetime

# Symbols for Nifty and Sensex
symbols = {
    "NIFTY 50": "^NSEI",
    "SENSEX": "^BSESN"
}

def get_ai_signal(name, ticker):
    try:
        # 5-minute interval data for last 2 days
        data = yf.download(tickers=ticker, period='2d', interval='5m', progress=False)
        if data.empty:
            return f"{name}: Market Closed/No Data"

        # --- AI Strategy Logic ---
        # 1. EMA 9 (Trend Filter)
        data['EMA_9'] = data['Close'].ewm(span=9, adjust=False).mean()
        
        # 2. RSI 14 (Momentum)
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / (loss + 1e-10)
        rsi = 100 - (100 / (1 + rs))

        curr_price = data['Close'].iloc[-1]
        last_ema = data['EMA_9'].iloc[-1]
        last_rsi = rsi.iloc[-1]

        # Signal Generation
        signal = "WAIT/SIDEWAYS"
        emoji = "⚪"
        
        if curr_price > last_ema and last_rsi > 55:
            signal = "STRONG BUY (UP)"
            emoji = "🚀"
        elif curr_price < last_ema and last_rsi < 45:
            signal = "STRONG SELL (DOWN)"
            emoji = "🔻"
        
        return f"{emoji} {name} | Price: {curr_price:.2f} | RSI: {last_rsi:.1f} | Signal: {signal}"

    except Exception as e:
        return f"Error in {name}: {str(e)}"

if __name__ == "__main__":
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n--- AI MARKET REPORT ({now}) ---")
    for name, ticker in symbols.items():
        print(get_ai_signal(name, ticker))
    print("-----------------------------------\n")
    
    
 
    
