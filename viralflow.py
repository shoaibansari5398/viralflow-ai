#!/usr/bin/env python3
import sys
import requests
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="ViralFlow AI CLI")
    parser.add_argument("url", help="The GitHub, YouTube, or Doc URL to process")
    parser.add_argument("--api", default="http://localhost:8000", help="ViralFlow API URL")
    
    args = parser.parse_args()
    
    try:
        response = requests.post(f"{args.api}/generate", json={"url": args.url})
        if response.status_code == 200:
            data = response.json()
            print("\n🚀 ViralFlow AI: Generated Thread\n" + "="*30)
            for i, tweet in enumerate(data['thread'], 1):
                print(f"{i}/ {tweet}\n")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Connection Error: {e}. Make sure the FastAPI server is running.")

if __name__ == "__main__":
    main()
