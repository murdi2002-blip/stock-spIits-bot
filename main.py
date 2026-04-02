
import requests
import pandas as pd
from datetime import datetime
import io

# بياناتك الجاهزة
TOKEN = "8621516305:AAFKRJBhdwYUYbX3s13mZj8H2SZ2f-iBxzc"
CHAT_ID = "-1003766698511" 

def run_bot():
    url = "https://stockanalysis.com/actions/splits/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        df = pd.read_html(response.text)[0]
        today = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        summary = f"🔄 *تحديث آلي لتقسيم الأسهم*\n⏰ الوقت: {today}\n\n"
        for index, row in df.head(5).iterrows():
            summary += f"🔹 {row['Symbol']} | {row['Date']} | {row['Ratio']}\n"

        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": summary, "parse_mode": "Markdown"})
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendDocument", 
                      data={"chat_id": CHAT_ID}, 
                      files={'document': (f'Splits_{today}.xlsx', output)})
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_bot()
