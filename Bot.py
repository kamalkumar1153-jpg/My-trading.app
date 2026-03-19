
 import time, requests, json
from nsepython import *

# अपना Firebase URL यहाँ डालें
FB_URL = "https://your-project-id.firebaseio.com/market_data.json"

def run():
    try:
        data = nse_optionchain_scrapper('NIFTY')
        pcr = round(data['records']['totalPutOI'] / data['records']['totalCallOI'], 2)
        status = "BULLISH 🚀" if pcr > 1.1 else "BEARISH 📉" if pcr < 0.9 else "NEUTRAL ↔️"
        
        payload = {"pcr": pcr, "status": status}
        requests.put(FB_URL, json.dumps(payload))
        print(f"Updated: {pcr}")
    except: print("Error fetching data")

if __name__ == "__main__":
    run()
    
