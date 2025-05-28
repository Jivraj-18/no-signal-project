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
generate natural language response from the given user query
"""

class NaturalLanguageResponseGenerator:
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


    async def natural_language_response_generator(self, information: str, system_prompt: str) -> str:
        response = await self._call_llm({
            "api_key": self.api_key,
            "model_id": "claude-3.5-sonnet",
            "prompt": f"Information: {information} \n\n  {system_prompt}",
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
    task_classifier = TaskClassifier()
    user_query = "Which inventory items qualify as no-movers according to our policy, and how many do we currently have?"
    system_prompt = system_prompt

    # Run the async function
    sql_query = asyncio.run(task_classifier.classify_via_llm(user_query, system_prompt))
    print(sql_query)