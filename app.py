from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
import json

app = FastAPI(title="ViralFlow AI API")

class ContentRequest(BaseModel):
    url: str

@app.get("/")
def read_root():
    return {"status": "ViralFlow AI is Live", "version": "0.1.0"}

@app.post("/generate")
def generate_content(request: ContentRequest):
    # Call the ingestion script
    try:
        # Ingest content
        ingest_res = subprocess.run(
            ["python3", "core/ingest.py", request.url],
            capture_output=True, text=True, check=True
        )
        content = ingest_res.stdout
        
        if not content or "Error" in content:
            raise HTTPException(status_code=400, detail="Failed to ingest URL content")
            
        # For now, simulate the LLM call using a template
        # Next step: Integrate actual xAI/Gemini API call
        viral_thread = [
            f"The truth about {request.url.split('/')[-1]} is hidden in the receipts.",
            "I spent 4 hours digging so you don't have to.",
            f"Key Technical Receipt: {content[:100]}...",
            "The Play: Stop overcomplicating your builds. Use this instead.",
            "Follow @Shoaib05 for more Agent Army builds. 🤖"
        ]
        
        return {
            "source_url": request.url,
            "thread": viral_thread,
            "status": "Success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
