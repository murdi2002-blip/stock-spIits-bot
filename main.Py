import requests
import pandas as pd
from datetime import datetime
import io

# --- بياناتك الخاصة (جاهزة) ---
TOKEN = "8621516305:AAFKRJBhdwYUYbX3s13mZj8H2SZ2f-iBxzc"
CHAT_ID = "-1003766698511" 

def send_update():
    # رابط سحب بيانات تقسيم الأسهم
    url = "https://stockanalysis.com/actions/splits/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        # 1. سحب البيانات
        response = requests.get(url, headers=headers)
        df = pd.read_html(response.text)[0]
        
        # 2. تجهيز الوقت والرسالة
        today = datetime.now().strftime("%Y-%m-%d %H:%M")
        summary = f"🔄 *تحديث آلي لتقسيم الأسهم*\n⏰ الوقت: {today}\n\n"
        
        # أخذ أول 5 صفوف فقط للرسالة المختصرة
        for index, row in df.head(5).iterrows():
            summary += f"🔹 {row['Symbol']} | {row['Date']} | {row['Ratio']}\n"

        # 3. إرسال الرسالة النصية للتليجرام
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": summary, "parse_mode": "Markdown"})
        
        # 4. تحويل الجدول بالكامل لملف إكسل وإرساله
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)
        
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendDocument", 
                      data={"chat_id": CHAT_ID}, 
                      files={'document': (f'Stock_Splits_{today}.xlsx', output)})
        
        print("✅ تم الإرسال بنجاح!")
        
    except Exception as e:
        print(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    send_update()
