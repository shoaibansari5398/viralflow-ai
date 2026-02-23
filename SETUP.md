# Setup & Usage: ViralFlow AI

## Prerequisites
- Python 3.8+
- `yt-dlp` (for YouTube transcripts)
- xAI API Key (set as `XAI_API_KEY`)

## Quick Start
1. **Clone & Install:**
   ```bash
   pip install fastapi uvicorn requests beautifulsoup4 yt-dlp
   ```
2. **Start the API:**
   ```bash
   python3 app.py
   ```
3. **Generate Content (CLI):**
   In a new terminal:
   ```bash
   python3 viralflow.py [URL]
   ```

## Supported Sources
- **GitHub:** Ingests README.md (main/master).
- **YouTube:** Extracts auto-generated transcripts.
- **Docs/Web:** Scrapes clean text content.

## Output
- 🧵 **X Thread:** 5-7 tweets using "Viper" logic.
- 📄 **LinkedIn Post:** Long-form technical receipts style.
