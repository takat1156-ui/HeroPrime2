import os
from fastapi import FastAPI, HTTPException
import google.generativeai as genai

app = FastAPI()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMINI_KEY")
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "Amin 1392 1 14")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# مسیر جدید برای عیب‌یابی دقیق
@app.get("/list-models")
def list_models():
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="No API Key found")
    try:
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        return {"available_models": available_models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# مسیر اصلی چت (ساده شده برای تست)
from pydantic import BaseModel
class ChatRequest(BaseModel):
    prompt: str
    user_name: str = "امین"
    token: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    if req.token != PROXY_TOKEN:
        raise HTTPException(status_code=401, detail="توکن نامعتبر است!")
    
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="API Key missing")

    try:
        # فعلاً از یک مدل بسیار پایه استفاده می‌کنیم
        model = genai.GenerativeModel('gemini-pro') 
        response = model.generate_content(req.prompt)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat Error: {str(e)}")

@app.get("/")
def home():
    return {"status": "HeroPrime Server is Running!"}
