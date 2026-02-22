from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os

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
        result = subprocess.run(
            ["python3", "core/ingest.py", request.url],
            capture_output=True, text=True, check=True
        )
        content = result.stdout
        
        if not content or "Error" in content:
            raise HTTPException(status_code=400, detail="Failed to ingest URL content")
            
        # Placeholder for LLM hook generation logic
        return {
            "source_url": request.url,
            "raw_content_preview": content[:200] + "...",
            "message": "Content ingested. Hook generation pending LLM integration."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
