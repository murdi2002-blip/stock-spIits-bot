import requests
import pandas as pd
from datetime import datetime
import io

# البيانات الخاصة بالبوت والقناة
TOKEN = "8621516305:AAFKRJBhdwYUYbX3s13mZj8H2SZ2f-iBxzc"
CHAT_ID = "-1006564128804" 

def run_bot():
    url = "https://stockanalysis.com/actions/splits/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        # جلب البيانات
        response = requests.get(url, headers=headers)
        df = pd.read_html(response.text)[0]
        
        # وقت التحديث
        today = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # تجهيز نص الرسالة
        summary = f"🔄 *تحديث تقسيم الأسهم*\n⏰ الوقت: {today}\n\n"
        summary += "يتم الآن إرسال الملف التفصيلي لآخر التحديثات..."

        # 1. إرسال الرسالة النصية
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": summary, "parse_mode": "Markdown"}
        )

        # 2. تجهيز ملف الإكسل وإرساله
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)

        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendDocument",
            data={"chat_id": CHAT_ID},
            files={'document': (f'Splits_{today}.xlsx', output)}
        )
        
        print("✅ تم إرسال البيانات بنجاح!")
        
    except Exception as e:
        print(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    run_bot()
