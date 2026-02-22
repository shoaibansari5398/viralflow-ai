import os
import sys
import subprocess
import requests
from bs4 import BeautifulSoup

def get_github_readme(repo_url):
    """Extracts README content from a GitHub repo."""
    # Convert to raw URL if needed
    if "github.com" in repo_url:
        repo_url = repo_url.replace("github.com", "raw.githubusercontent.com")
        if not repo_url.endswith("/master/README.md") and not repo_url.endswith("/main/README.md"):
            # Try main then master
            for branch in ["main", "master"]:
                test_url = f"{repo_url.rstrip('/')}/{branch}/README.md"
                res = requests.get(test_url)
                if res.status_code == 200:
                    return res.text
    return "Could not fetch README."

def get_youtube_transcript(video_url):
    """Fetches YouTube transcript using yt-dlp."""
    try:
        # Get transcript using yt-dlp
        cmd = ["yt-dlp", "--get-subs", "--skip-download", "--write-auto-subs", "--sub-format", "vtt", "-o", "transcript", video_url]
        subprocess.run(cmd, check=True, capture_output=True)
        
        # Find the transcript file
        for f in os.listdir("."):
            if f.startswith("transcript") and f.endswith(".vtt"):
                with open(f, 'r') as file:
                    content = file.read()
                os.remove(f)
                return content
    except Exception as e:
        return f"Error fetching YouTube transcript: {str(e)}"
    return "No transcript found."

def get_web_content(url):
    """Generic web scraper for documentation/articles."""
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        # Simple extraction: remove scripts and styles, then get text
        for script in soup(["script", "style"]):
            script.extract()
        return soup.get_text(separator='\n', strip=True)
    except Exception as e:
        return f"Error fetching web content: {str(e)}"

if __name__ == "__main__":
    url = sys.argv[1]
    if "github.com" in url:
        print(get_github_readme(url))
    elif "youtube.com" in url or "youtu.be" in url:
        print(get_youtube_transcript(url))
    else:
        print(get_web_content(url))
