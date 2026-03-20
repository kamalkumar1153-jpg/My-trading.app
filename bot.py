import yfinance as yf
import pandas_ta as ta
import requests
import os

# GitHub Secrets se data lena
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

def send_telegram_msg(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}&parse_mode=Markdown"
    requests.get(url)

def get_signal(symbol, name):
    # Live data fetch karna (5 min interval)
    df = yf.download(symbol, period="1d", interval="5m")
    if df.empty: return

    # Indicators calculate karna
    df['EMA20'] = ta.ema(df['Close'], length=20)
    df['RSI'] = ta.rsi(df['Close'], length=14)

    last_row = df.iloc[-1]
    price = last_row['Close']
    ema = last_row['EMA20']
    rsi = last_row['RSI']

    # --- AI SIGNAL LOGIC ---
    # Buy: Price EMA ke upar aur RSI 50+ (Bullish Momentum)
    if price > ema and rsi > 55:
        send_telegram_msg(f"🚀 *BUY SIGNAL: {name}*\n💰 Price: {price:.2f}\n📈 RSI: {rsi:.2f}\n✅ Trend: Bullish")
    
    # Sell: Price EMA ke niche aur RSI 45- (Bearish Momentum)
    elif price < ema and rsi < 45:
        send_telegram_msg(f"🔻 *SELL SIGNAL: {name}*\n💰 Price: {price:.2f}\n📉 RSI: {rsi:.2f}\n❌ Trend: Bearish")

# Nifty 50 aur Sensex check karein
get_signal("^NSEI", "NIFTY 50")
get_signal("^BSESN", "SENSEX")


    
    
 
    
