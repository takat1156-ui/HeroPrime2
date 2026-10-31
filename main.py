import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

# تنظیمات API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMINI_KEY")
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "Amin 1392 1 14")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# انتخاب مدل از لیست دقیق تو (Gemini 3.5 Flash)
# این مدل در لیست تو بود و بسیار قدرتمند است
MODEL_NAME = 'gemini-3.5-flash'

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
        # مقداردهی مدل با نام دقیق از لیست تو
        model = genai.GenerativeModel(MODEL_NAME)
        
        full_prompt = f"You are HeroPrime, a highly intelligent AI assistant for {req.user_name}. User says: {req.prompt}"
        
        response = model.generate_content(full_prompt)
        
        if response and response.text:
            return {"response": response.text}
        else:
            raise HTTPException(status_code=500, detail="Empty response from Google.")
            
    except Exception as e:
        # اگر باز هم ارور داد، متن دقیق رو برگردون
        raise HTTPException(status_code=500, detail=f"Chat Error: {str(e)}")

@app.get("/")
def home():
    return {"status": "HeroPrime Ultra-Advanced Server is Running!", "model_used": MODEL_NAME}
