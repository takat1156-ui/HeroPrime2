import os
from fastapi import FastAPI, Header, HTTPException
import google.generativeai as genai
from pydantic import BaseModel

app = FastAPI(title="HeroPrime AI Server")

# دریافت کلیدها از تنظیمات سرور رندر
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "amin1405")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# استفاده از مدل سریع و قدرتمند جمینی
MODEL_NAME = "gemini-1.5-flash"

class ChatRequest(BaseModel):
    prompt: str
    user_name: str = "دوست من"  # اگر اسمی نفرستاد، پیش‌فرض این باشه
    token: str = None

@app.get("/")
def home():
    return {"status": "HeroPrime Server is Online! 🚀", "developer": "Amin"}

@app.post("/chat")
def chat_with_heroprime(req: ChatRequest, authorization: str = Header(None)):
    # بررسی توکن امنیتی برای جلوگیری از دسترسی غریبه‌ها
    token = req.token or authorization
    if token != PROXY_TOKEN:
        raise HTTPException(status_code=401, detail="توکن امنیتی نامعتبر است!")
    
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="کلید جمینی روی سرور تنظیم نشده است.")

    try:
        # شخصیت هیروپرایم با قابلیت دریافت و استفاده از نام کاربر
        system_instruction = (
            f"تو هیروپرایم هستی؛ یک هوش مصنوعی بسیار باهوش، حرفه‌ای، مهربان، صمیمی و کاملاً حامی. "
            f"مخاطبی که الان با او صحبت می‌کنی نامش '{req.user_name}' است. حتماً در پاسخ‌ها او را با نام خودش صدا بزن. "
            f"همیشه با دقت، باادب، ساختاریافته و به زبان فارسی روان جواب بده. "
            f"تو دستیارِ قابل‌اعتمادِ امین (سازنده اصلی‌ات) هستی."
        )
        
        generation_config = {
            "temperature": 0.7,
        }

        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            system_instruction=system_instruction,
            generation_config=generation_config
        )
        
        response = model.generate_content(req.prompt)
        return {"response": response.text}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
