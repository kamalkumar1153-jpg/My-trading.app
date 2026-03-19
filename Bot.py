import time
import requests
import json
from nsepython import *

# 1. अपना असली Firebase URL यहाँ डालें (अंत में market_data.json ज़रूर लगाएँ)
FIREBASE_URL = "https://your-project-id.firebaseio.com/market_data.json"

def get_market_sentiment():
    try:
        # NSE से निफ्टी ऑप्शन चेन का डेटा लें
        print("Fetching NSE Data...")
        oi_data = nse_optionchain_scrapper('NIFTY')
        
        total_put_oi = oi_data['records']['totalPutOI']
        total_call_oi = oi_data['records']['totalCallOI']
        
        # PCR कैलकुलेशन
        pcr = round(total_put_oi / total_call_oi, 2)
        
        # प्रोबेबिलिटी और स्टेटस लॉजिक
        probability = 50
        status = "NEUTRAL ↔️"
        
        if pcr > 1.25:
            status = "STRONG BUY 🚀 (UP)"
            probability = 85
        elif pcr > 1.05:
            status = "BUY 📈"
            probability = 65
        elif pcr < 0.75:
            status = "STRONG SELL 🔴 (DOWN)"
            probability = 80
        elif pcr < 0.95:
            status = "SELL 📉"
            probability = 60

        # Firebase के लिए डेटा पैकेट तैयार करें
        payload = {
            "pcr": pcr,
            "status": status,
            "probability": probability,
            "last_update": time.strftime("%H:%M:%S")
        }

        # Firebase पर डेटा अपलोड करें (PUT request)
        response = requests.put(FIREBASE_URL, json.dumps(payload))
        
        if response.status_code == 200:
            print(f"✅ Success! PCR: {pcr} | Status: {status}")
        else:
            print(f"❌ Firebase Error: {response.status_code}")

    except Exception as e:
        print(f"⚠️ Error: {e}")

# लूप: हर 5 मिनट में डेटा अपडेट करें (NSE की पाबंदी के कारण 3-5 min सही है)
if __name__ == "__main__":
    while True:
        get_market_sentiment()
        time.sleep(300) 
      
