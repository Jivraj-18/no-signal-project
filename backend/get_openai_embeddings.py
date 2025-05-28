# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx",
#    "python-dotenv",
# ]
# ///


embeddings_url = "http://aiproxy.sanand.workers.dev/openai/v1/embeddings"
from dotenv import load_dotenv
load_dotenv()
import os 
open_ai_api_key = os.getenv("AIPROXY_KEY")
import httpx

client = httpx.Client()

async def get_embeddings(text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {open_ai_api_key}",
    }
    data = {
        "model": "text-embedding-3-small",
        "input": text,
    }


    async with httpx.AsyncClient() as client:
        response = await client.post(embeddings_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
