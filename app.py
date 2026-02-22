from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
import json
import requests

app = FastAPI(title="ViralFlow AI API")

XAI_API_KEY = os.getenv("XAI_API_KEY")

class ContentRequest(BaseModel):
    url: str

@app.get("/")
def read_root():
    return {"status": "ViralFlow AI is Live", "version": "0.1.0"}

def call_grok(prompt):
    if not XAI_API_KEY:
        return None
    try:
        url = "https://api.x.ai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {XAI_API_KEY}"
        }
        data = {
            "model": "grok-beta",
            "messages": [{"role": "system", "content": "You are ViralFlow AI. Convert technical content into viral X threads using blunt hooks and technical receipts."}, {"role": "user", "content": prompt}],
            "stream": False
        }
        res = requests.post(url, headers=headers, json=data)
        return res.json()['choices'][0]['message']['content']
    except Exception:
        return None

@app.post("/generate")
def generate_content(request: ContentRequest):
    try:
        ingest_res = subprocess.run(
            ["python3", "core/ingest.py", request.url],
            capture_output=True, text=True, check=True
        )
        content = ingest_res.stdout
        
        if not content or "Error" in content:
            raise HTTPException(status_code=400, detail="Failed to ingest URL content")
            
        prompt = f"Create a viral X thread (5-7 tweets) based on this content:\n\n{content[:2000]}"
        grok_response = call_grok(prompt)
        
        if grok_response:
            # Simple split by numbered list or newlines for now
            thread = [t.strip() for t in grok_response.split('\n\n') if t.strip()]
        else:
            # Fallback to template if API fails or key is missing
            thread = [
                f"The truth about {request.url.split('/')[-1]} is hidden in the receipts.",
                "I spent 4 hours digging so you don't have to.",
                f"Key Technical Receipt: {content[:100]}...",
                "The Play: Stop overcomplicating your builds. Use this instead.",
                "Follow @Shoaib05 for more Agent Army builds. 🤖"
            ]
        
        return {
            "source_url": request.url,
            "thread": thread,
            "status": "Success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
