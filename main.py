import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

# دریافت کلید با هر دو نام ممکن
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMINI_KEY")
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "Amin 1392 1 14")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# تغییر مدل به نسخه بسیار پایدار و عمومی gemini-pro
try:
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    print(f"Error initializing model: {e}")

class ChatRequest(BaseModel):
    prompt: str
    user_name: str = "امین"
    token: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    if req.token != PROXY_TOKEN:
        raise HTTPException(status_code=401, detail="توکن نامعتبر است!")
    
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="API Key not found on server")
        
    try:
        # ساخت پرامپت به سبک جدید برای جلوگیری از خطای ساختاری
        full_prompt = f"You are HeroPrime, a helpful AI assistant for {req.user_name}. User says: {req.prompt}"
        
        response = model.generate_content(full_prompt)
        
        # بررسی اینکه آیا پاسخ واقعاً متنی هست یا نه
        if response and response.text:
            return {"response": response.text}
        else:
            raise HTTPException(status_code=500, detail="Google returned an empty response.")
            
    except Exception as e:
        # اینجا خیلی مهمه که دقیقاً بگیم ارور چیه
        raise HTTPException(status_code=500, detail=f"Google API Error: {str(e)}")

@app.get("/")
def home():
    return {"status": "HeroPrime Server is Running!", "status_code": 200}
