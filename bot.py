import yfinance as yf
import pandas_ta as ta
import json
from datetime import datetime

def get_signals(symbol):
    # Nifty और Sensex के लिए सही सिंबल
    t_sym = "^NSEI" if symbol == "NIFTY" else "^BSESN"
    ticker = yf.Ticker(t_sym)
    df = ticker.history(period="5d", interval="15m") # 15m प्रेडिक्शन
    
    if df.empty: return None

    # इंडिकेटर्स कैलकुलेशन
    df['EMA_20'] = ta.ema(df['Close'], length=20)
    df['RSI'] = ta.rsi(df['Close'], length=14)
    macd = ta.macd(df['Close'])
    df['MACD_H'] = macd['MACDh_12_26_9']
    df['Pivot'] = (df['High'] + df['Low'] + df['Close']) / 3
    
    latest = df.iloc[-1]
    
    # 15m Trend Logic
    trend = "NEUTRAL"
    if latest['Close'] > latest['EMA_20'] and latest['MACD_H'] > 0 and latest['RSI'] < 70:
        trend = "BULLISH"
    elif latest['Close'] < latest['EMA_20'] and latest['MACD_H'] < 0 and latest['RSI'] > 30:
        trend = "BEARISH"
    
    return {
        "price": round(latest['Close'], 2),
        "rsi": round(latest['RSI'], 1),
        "macd_h": round(latest['MACD_H'], 2),
        "pivot": round(latest['Pivot'], 2),
        "trend": trend,
        "time": datetime.now().strftime('%H:%M:%S')
    }

# डेटा को JSON में सेव करना
all_market_data = {
    "nifty": get_signals("NIFTY"),
    "sensex": get_signals("SENSEX")
}

with open('data.json', 'w') as f:
    json.dump(all_market_data, f)




                          

    
    
 
    
