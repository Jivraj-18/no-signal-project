# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx",
#    "python-dotenv",
# ]
# ///
from dotenv import load_dotenv
load_dotenv()
import os 
import json
base_url = os.getenv("Syn_LLM_URL")

Syn_LLM_API_KEY = os.getenv("Syn_LLM_API_KEY")
import httpx

async def get_embeddings(text):
    headers = {"Content-Type": "application/json"}
    data = {
        "api_key": Syn_LLM_API_KEY,
        "model_id": "amazon-embedding-v2",
        "prompt": text,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(base_url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
