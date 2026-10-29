from fastapi import FastAPI, Request
import httpx, os, json

app = FastAPI()
GEMINI_KEY = os.environ.get("GEMINI_KEY")
PROXY_TOKEN = os.environ.get("PROXY_TOKEN")

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/v1/chat")
async def chat(request: Request):
    data = await request.json()
    if request.headers.get("x-proxy-token") != PROXY_TOKEN:
        return {"error": "unauthorized"}, 401
    text = data.get("text", "")
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=" + GEMINI_KEY
    async with httpx.AsyncClient(timeout=60) as c:
        r = await c.post(url, json={"contents": [{"parts": [{"text": text}]}]})
        j = r.json()
    try:
        reply = j["candidates"][0]["content"]["parts"][0]["text"]
    except:
        reply = "خطا"
    return {"reply": reply}
