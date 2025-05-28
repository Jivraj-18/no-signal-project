# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fastapi",
#   "uvicorn",
#   "httpx",
#    "numpy",
#   "modin",
#   "modin[ray]",
#    "python-multipart",
#    "python-dotenv",
#     "starlette",
#     "itsdangerous",
#     "duckdb",
#     "pandas"
# ]
# ///
import sqlite3
from urllib.parse import urlencode
import duckdb
import modin.pandas as pd
import json
from fastapi import FastAPI, Form, Request
from get_amazon_embeddings import get_embeddings
from calculate_cosine_similarity import cosine_similarity
from services.task_classify import TaskClassifier
from services.summaries_rag_output import Rag_output_summarizer
from services.generate_sql import SQLGenerator
from services.check_if_request_should_proceed import Classify_User_query
from services.generate_response import NaturalLanguageResponseGenerator
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from starlette.requests import Request
import os 
import httpx
import asyncio
app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="your-secret",
    session_cookie="session",
    same_site="lax",   # 👈 allow cross-origin
    https_only=False    # 👈 True if using HTTPS
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8080","http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")


@app.get("/login")
async def login():
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    url = f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"
    print(f"Redirecting to: {url}")
    return RedirectResponse(url=url)

@app.get("/auth/callback")
async def auth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "No code provided"}

    # Exchange the authorization code for an access token
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        token_response = response.json() 
        access_token = token_response.get("access_token")
        id_token = token_response.get("id_token")
        if not access_token or not id_token:
            return {"error": "Failed to obtain access token"}
        
        headers = { 
            "Authorization": f"Bearer {access_token}"
        }
        user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        user_info_response = await client.get(user_info_url, headers=headers)
        user_info = user_info_response.json()
        request.session['name'] = user_info.get("name")
        request.session['email'] = user_info.get("email")
        request.session['access_token'] = access_token
        request.session['id_token'] = id_token
        return RedirectResponse(url="http://127.0.0.1:8080/ask")

@app.get("/logout")
async def logout(request: Request):
    access_token = request.session.get("access_token")
    if access_token:
        revoke_url = "https://oauth2.googleapis.com/revoke"
        params = {
            "token": access_token,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET
        }
        async with httpx.AsyncClient() as client:
            await client.post(revoke_url, params=params)
    request.session.clear()
    return RedirectResponse(url="/")


@app.get("/")
async def root():
    return 
    """
    <html>
    <body>
    <a href="/login">Login with Google</a>
    </body>
    </html>
    """

# create a endpoint /process that takes a question as form data 
@app.post("/process")
async def process_question(
    request: Request,
    question: str = Form(None),  # Make it optional
    ):
    print(question)
    tokens = {
        "input_tokens": 0,
        "output_tokens": 0,
    }
# async def process_question(
#     # request: Request,
#     question: str #= Form(None),  # Make it optional
#     ):    
    if request.session.get('email') is None:
        return {"error": "login required"}
    user_conn = sqlite3.connect('users_data.db')
    user_cursor = user_conn.cursor()
    user_cursor.execute("SELECT * FROM users WHERE email = ?", (request.session.get('email'),))
    exists = user_cursor.fetchone()
    
    if  exists is None:       
        # instert the user into the database
        user_cursor.execute(
            "INSERT INTO users (email, type) VALUES (?, ?)",
            (request.session.get('email'), 'customer')
        )
        request.session['type'] = 'customer'
        user_conn.commit()
        user_conn.close()
    else : 
 
        request.session['type'] = exists[1]
        print(exists)
        user_conn.close()
    print(exists[1])
    classify_user_query = Classify_User_query()
    with open("user_classification_prompt.txt") as f :
        user_classification_prompt = f.read()
    user_type = json.loads((await classify_user_query.classify_user_query(question, user_classification_prompt))['response']['content'][0]['text'])['category']
      
    # user_type = json.loads((await classify_user_query.classify_user_query(question, user_classification_prompt))['response']['content'][0]['text'])['category']
    print(user_type)
    print(request.session['type'])
    if user_type != request.session['type']:
        return {"error": "You don't hae permission to access this resource. Please contact your administrator."}

    task_classifier = TaskClassifier()
    user_query = question
    with open("classification_prompt.txt") as f :
        classification_prompt = f.read()
    

    output =  []
    # Run the async function
    steps = json.loads((await task_classifier.classify_via_llm(user_query, classification_prompt))['response']['content'][0]['text'])
    print(steps)
    for step in steps:
        if step['type'] == 'rag':
            similarities = []
            embeddings = await get_embeddings(question)
            embeddings_data = embeddings["response"]['embedding']
            with open("embeddings_amazon.json", "r") as file:
                collection = json.load(file)
            for embedding in collection['embeddings']:
                similarity = cosine_similarity(embeddings_data, embedding['embedding'])
                similarities.append({
                    "text": embedding['text'],
                    "source": embedding['source'],
                    "similarity": similarity
                })
            similarities = sorted(similarities, key=lambda x: x['similarity'], reverse=True)
            # return similarities
            summarizer = Rag_output_summarizer()
            user_query = f"""
                Output from RAG: {similarities}
                User Query: {step['current_task']}
            """
            # store response to a file under response directory, file id should be current timestamp
            with open(f"response/{step['current_task']}_{int(pd.Timestamp.now().timestamp())}.json", "w") as f:
                json.dump(similarities, f, indent=4)
            rag_output = (await summarizer.classify_via_llm(user_query, "You will be provided with rag's output, your task it to summarize the output in a concise manner for the user query."))['response']['content'][0]['text']  
            
            # return {"rag_output": rag_output}
            output.append({
                "step":"rag",
                "output":rag_output
            })
        elif step['type'] == 'nl_to_sql':
            user_query = f"""
                Task That needs to be done :{step['current_task']}, 
                Additional context relevant to the task: {output[-1]['output'] if output else ''}
            """ 
            sql_generator = SQLGenerator()
            with open("sql_generation_prompt.txt") as f:
                sql_generator.system_prompt = f.read()
            
            
            try :
                sql_query = await sql_generator.generate_sql_via_llm(user_query, sql_generator.system_prompt)
                data = sql_generator.fetch_data(sql_query)
                with open(f"response/{step['current_task']}_{int(pd.Timestamp.now().timestamp())}.json", "w") as f:
                    json.dump(data.to_dict(orient='records'), f, indent=4)
                output.append({
                    "step": "nl_to_sql",
                    "output": data.to_dict(orient='records')  # Convert DataFrame to list of dicts
                })
                print(data)
            except Exception as e:
                # log the error to a file 
                with open("sql_error.log", "a") as f:
                    f.write(f"Error executing SQL query: {str(e)}\n")
            
            
            # return {"sql_query": sql_query}
        elif step['type'] == 'generate_response':
            nl_response_generator = NaturalLanguageResponseGenerator()
            rag_output = [obj for obj in output if obj["step"] == "rag"]
            nl_output = [out for out in output if out["step"] == "nl_to_sql"]
            if rag_output:
                natural_language_response = (await nl_response_generator.natural_language_response_generator(f"""Task : {step['current_task']} \n Relevant  Information : {output}  """, "generate natural language response from the given user query"))['response']['content'][0]['text']
            else : 
                natural_language_response = ''
            # write json object to a file {"natural_language_response": natural_language_response, "nl_output": nl_output}
            with open(f"response/{step['type']}_{step['current_task']}.json", "w") as f:
                json.dump({"natural_language_response": natural_language_response, "nl_output": nl_output}, f, indent=4)
            return {"natural_language_response": natural_language_response, "nl_output": nl_output}
        else:
            step['task'] = "Unknown task type."
    return {"steps": steps}



if __name__ == "__main__":
    import uvicorn
    # df = pd.read_csv('sample_questions.csv')
    # # pass through each row of dataframe and store the response of process_question in a new column
    # df['response'] = df.apply(lambda row: asyncio.run(process_question(row['Question'])), axis=1)
    # # save the dataframe to a csv file
    # df.to_csv('question_response.csv', index=False)
    uvicorn.run(app, host="0.0.0.0", port=8000)