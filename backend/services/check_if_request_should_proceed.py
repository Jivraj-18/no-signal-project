# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pandas",
#   "chardet",
#    "python-dotenv",
#     "httpx",
# ]
# ///

from dotenv import load_dotenv
import os
import httpx
import json

system_prompt = """
    Given the user query, classify the user query into one of the following categories:
    1. financial 
    2. inventory
    3. sales
    4. customer

    Your response should be a single JSON object with two keys: "category" and "reason". The "category" key must contain only the category name, using the categories listed above. Do not include any code blocks, markdown, comments, or extra text. Only return the JSON object — any other content will be treated as incorrect.
"""

class Classify_User_query:
    def __init__(self):
        load_dotenv()
        self.base_url = os.getenv("Syn_LLM_URL")
        self.api_key = os.getenv("Syn_LLM_API_KEY")
        self.headers = {"Content-Type": "application/json"}

    async def _call_llm(self, data: dict) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, headers=self.headers,  data=json.dumps(data), timeout=60.0)
            response.raise_for_status()
            return response.json()


    async def classify_user_query(self, user_query: str, system_prompt: str) -> str:
        response = await self._call_llm({
            "api_key": self.api_key,
            "model_id": "claude-3.5-sonnet",
            "prompt": f"User query: {user_query} \n\n  {system_prompt}",
        })
        # write response to a file 
        # with open("response_class.json", "w") as f:
        #     json.dump(response, f, indent=4)
        try :
            return response 
        except Exception as e:
            raise Exception(f"Error generating SQL: {response.get('error', e)}")

if __name__ == "__main__":
    import asyncio
    classify_user = Classify_User_query()
    user_query = "Which inventory items qualify as no-movers according to our policy, and how many do we currently have?"
    system_prompt = system_prompt

    # Run the async function
    sql_query = asyncio.run(classify_user.classify_user_query(user_query, system_prompt))
    print(sql_query)