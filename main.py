import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

# خواندن هوشمند کلید جمینی از هر نامی که در محیط سرور باشد
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMINI_KEY")
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "Amin 1392 1 14")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# مدل جمینی
model = genai.GenerativeModel('gemini-1.5-flash')

class ChatRequest(BaseModel):
    prompt: str
    user_name: str = "امین"
    token: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    # بررسی صحت توکن
    if req.token != PROXY_TOKEN:
        raise HTTPException(status_code=401, detail="توکن نامعتبر است!")
    
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="کلید جمینی روی سرور تنظیم نشده است!")
        
    try:
        # ساخت پرامپت حرفه‌ای برای هیروپرایم
        full_prompt = f"تو یک دستیار هوش مصنوعی هوشمند و پیشرفته به نام هیروپرایم (HeroPrime) هستی. مخاطبِ تو {req.user_name} است. با لحنی مودبانه، صمیمی، حرفه‌ای و دقیق پاسخ بده.\n\nسوال کاربر: {req.prompt}"
        
        response = model.generate_content(full_prompt)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"status": "HeroPrime Server is Running!", "status_code": 200}
