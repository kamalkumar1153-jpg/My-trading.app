import yfinance as yf
import pandas_ta as ta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# CORS allow करें ताकि GitHub Pages या Localhost से डेटा फेच हो सके
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def fetch_signals(symbol):
    ticker_sym = "^NSEI" if symbol == "NIFTY" else "^BSESN"
    ticker = yf.Ticker(ticker_sym)
    # 15m ट्रेंड के लिए पिछला 5 दिन का डेटा
    df = ticker.history(period="5d", interval="15m")
    
    if df.empty: return None

    # इंडिकेटर्स कैलकुलेशन
    df['EMA_20'] = ta.ema(df['Close'], length=20)
    df['RSI'] = ta.rsi(df['Close'], length=14)
    macd = ta.macd(df['Close'])
    df['MACD_H'] = macd['MACDh_12_26_9']
    df['Pivot'] = (df['High'] + df['Low'] + df['Close']) / 3

    latest = df.iloc[-1]
    
    # 15m Prediction Logic
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
        "time": latest.name.strftime('%H:%M:%S')
    }

@app.get("/get-price/{symbol}")
async def get_data(symbol: str):
    data = fetch_signals(symbol.upper())
    return data if data else {"error": "No Data"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



                          

    
    
 
    
