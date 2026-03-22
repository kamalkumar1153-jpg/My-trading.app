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
import telebot
import requests
import time

# 1. Apni Details Daalein
API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID' # Idhar apni Chat ID daalein

bot = telebot.TeleBot(API_TOKEN)

def get_market_data():
    # Agar aapne dashboard mein Google Sheets use kiya hai
    # Toh yahan se aap Nifty/Sensex ka data fetch kar sakte hain
    # Abhi ke liye hum dummy data le rahe hain
    nifty_price = 23114.5  # Aapke screenshot ke mutabik
    rsi_value = 50.0
    return nifty_price, rsi_value

def send_alert():
    price, rsi = get_market_data()
    message = f"🚀 *AI Pro Terminal Update*\n\n" \
              f"📊 *NIFTY 50:* ₹{price}\n" \
              f"📈 *RSI:* {rsi}\n" \
              f"⏳ *Status:* NEUTRAL"
    
    bot.send_message(CHAT_ID, message, parse_mode='Markdown')

# Har 15 minute mein update bhejne ke liye
if __name__ == "__main__":
    print("Bot is running...")
    send_alert()
                          

    
    
 
    
