# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pandas",
#   "chardet",
#    "python-dotenv",
#     "httpx",
# ]
# ///
import sqlite3
from dotenv import load_dotenv
import os
import httpx
import json
import pandas as pd 
system_prompt = """
 # Natural Language to SQL Converter

You are an assistant that must return a single JSON object with one key: "sql_query". The "sql_query" key must contain only the raw SQL query, using JOINs instead of subqueries wherever possible. Do not include any code blocks, markdown, comments, or extra text. Only return the JSON object — any other content will be treated as incorrect.

Remember to generate only safe, read-only SQL queries that don't attempt to modify or access the database in unauthorized ways. Never include multiple SQL statements separated by semicolons. Only use SELECT statements.

## Database Schema

The database contains data parsed from IPL cricket match JSON files into a normalized relational schema:

 #   Column                         Non-Null Count   Dtype  
---  ------                         --------------   -----  
 0   Type                           180519 non-null  object 
 1   Days for shipping (real)       180519 non-null  int64  
 2   Days for shipment (scheduled)  180519 non-null  int64  
 3   Benefit per order              180519 non-null  float64
 4   Sales per customer             180519 non-null  float64
 5   Delivery Status                180519 non-null  object 
 6   Late_delivery_risk             180519 non-null  int64  
 7   Category Id                    180519 non-null  int64  
 8   Category Name                  180519 non-null  object 
 9   Customer City                  180519 non-null  object 
 10  Customer Country               180519 non-null  object 
 11  Customer Email                 180519 non-null  object 
 12  Customer Fname                 180519 non-null  object 
 13  Customer Id                    180519 non-null  int64  
 14  Customer Lname                 180511 non-null  object 
 15  Customer Password              180519 non-null  object 
 16  Customer Segment               180519 non-null  object 
 17  Customer State                 180519 non-null  object 
 18  Customer Street                180519 non-null  object 
 19  Customer Zipcode               180516 non-null  float64
 20  Department Id                  180519 non-null  int64  
 21  Department Name                180519 non-null  object 
 22  Latitude                       180519 non-null  float64
 23  Longitude                      180519 non-null  float64
 24  Market                         180519 non-null  object 
 25  Order City                     180519 non-null  object 
 26  Order Country                  180519 non-null  object 
 27  Order Customer Id              180519 non-null  int64  
 28  order date (DateOrders)        180519 non-null  object 
 29  Order Id                       180519 non-null  int64  
 30  Order Item Cardprod Id         180519 non-null  int64  
 31  Order Item Discount            180519 non-null  float64
 32  Order Item Discount Rate       180519 non-null  float64
 33  Order Item Id                  180519 non-null  int64  
 34  Order Item Product Price       180519 non-null  float64
 35  Order Item Profit Ratio        180519 non-null  float64
 36  Order Item Quantity            180519 non-null  int64  
 37  Sales                          180519 non-null  float64
 38  Order Item Total               180519 non-null  float64
 39  Order Profit Per Order         180519 non-null  float64
 40  Order Region                   180519 non-null  object 
 41  Order State                    180519 non-null  object 
 42  Order Status                   180519 non-null  object 
 43  Order Zipcode                  24840 non-null   float64
 44  Product Card Id                180519 non-null  int64  
 45  Product Category Id            180519 non-null  int64  
 46  Product Description            0 non-null       float64
 47  Product Image                  180519 non-null  object 
 48  Product Name                   180519 non-null  object 
 49  Product Price                  180519 non-null  float64
 50  Product Status                 180519 non-null  int64  
 51  shipping date (DateOrders)     180519 non-null  object 
 52  Shipping Mode                  180519 non-null  object 
"""

class SQLGenerator:
    def __init__(self):
        load_dotenv()
        self.base_url = os.getenv("Syn_LLM_URL")
        self.api_key = os.getenv("Syn_LLM_API_KEY")
        self.headers = {"Content-Type": "application/json"}
        self.db_path = "supply_data.db"
    async def _call_llm(self, data: dict) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, headers=self.headers,  data=json.dumps(data), timeout=60.0)
            response.raise_for_status()
            return response.json()


    async def generate_sql_via_llm(self, user_query: str, system_prompt: str) -> str:
        response = await self._call_llm({
            "api_key": self.api_key,
            "model_id": "claude-3.5-sonnet",
            "prompt": f"{system_prompt}\n\nUser Query: {user_query}",
        })
        # 
        try :
            return json.loads(response['response']['content'][0]['text'])['sql_query']
        except Exception as e:
            raise Exception(f"Error generating SQL: {response.get('error', e)}")
    def fetch_data(self, sql_query: str) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame"""
    
        try:
            # Use read_only connection for added security
            con = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(sql_query, con)

            con.close()
            # logger.info(f"Query executed successfully: {sql_query[:50]}...")
            return df
        except Exception as e:
            # logger.error(f"Error executing query: {str(e)}")
            raise
if __name__ == "__main__":
    import asyncio
    sql_generator = SQLGenerator()
    user_query = "Total sales value of all products in the year 2022"
    system_prompt = system_prompt

    # Run the async function
    sql_query = asyncio.run(sql_generator.generate_sql_via_llm(user_query, system_prompt))
    print(sql_query)