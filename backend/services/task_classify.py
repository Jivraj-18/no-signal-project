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
import pandas as pd 
system_prompt = """
You are an assistant that given an user query breaks down task into the chain in which task should be done, there are multiple tasks, you need to correctly create a chain for upcoming tasks. 

There are three types of tasks:
1. Only natural langugage to sql for Data-Based query
2. Only RAG for Document based Query 
3. Hybrid if query requires combining document and data-based 

Here is one example of hybrid query: 
User Query : 
Chain: Retrieve 'no-mover' definition from policy docs, extract conditions (e.g., 'no stock movement in 180 days'), generate SQL to count qualifying inventory items, and return the count with explanation of the applied criterie


Your response should strictly be a json array with each object having type(takes 3 values rag, nl_to_sql, generate_response), current_task(task for current). Don't generate anything else other than json array in your response. Your sql queries will be directly executed by a automated script. Execution of sql quries should not be part of your chain.

For helping RAG model, generate task in such a way that it helps RAG model accurately identify correct document. 
"""

class TaskClassifier:
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


    async def classify_via_llm(self, user_query: str, system_prompt: str) -> str:
        response = await self._call_llm({
            "api_key": self.api_key,
            "model_id": "claude-3.5-sonnet",
            "prompt": f"User Query: {user_query} \n\n  {system_prompt}",
        })
        # write response to a file 
        with open("response_class.json", "w") as f:
            json.dump(response, f, indent=4)
        try :
            return response 
        except Exception as e:
            raise Exception(f"Error generating SQL: {response.get('error', e)}")

if __name__ == "__main__":
    import asyncio
    task_classifier = TaskClassifier()

    user_query = "How much inventory do we currently have in the Southwest region?"
    system_prompt = system_prompt
    df = pd.read_csv('../sample_questions.csv')
    # pass through each row of dataframea and store the response of classify_via_llm in a new column 
    df['response'] = df.apply(lambda row: asyncio.run(task_classifier.classify_via_llm(row['Question'], system_prompt)), axis=1)
    # save the dataframe to a csv file
    df.to_csv('response_classification.csv', index=False)
    # Run the async function
    # sql_query = asyncio.run(task_classifier.classify_via_llm(user_query, system_prompt))
    print(sql_query)