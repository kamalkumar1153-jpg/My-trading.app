import yfinance as yf
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Frontend se connect karne ke liye CORS allow karein
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get-price/{symbol}")
def get_stock_price(symbol: str):
    # Indian stocks ke liye .NS (NSE) ya .BO (BSE) lagana zaruri hai
    ticker = yf.Ticker(f"{symbol}.NS")
    data = ticker.history(period="1d", interval="1m")
    
    if not data.empty:
        latest_price = data['Close'].iloc[-1]
        change = latest_price - data['Open'].iloc[0]
        p_change = (change / data['Open'].iloc[0]) * 100
        
        return {
            "symbol": symbol,
            "price": round(latest_price, 2),
            "change": round(change, 2),
            "p_change": round(p_change, 2)
        }
    return {"error": "Data not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


                          

    
    
 
    
