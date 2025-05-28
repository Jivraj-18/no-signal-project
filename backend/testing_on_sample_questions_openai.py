# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "modin",
#   "modin[ray]",
#   "python-dotenv",
#   "httpx",
#   "numpy",
# ]
# ///
import asyncio
import modin.pandas as pd
from dotenv import load_dotenv
load_dotenv()
import os 
import numpy as np  
import httpx
import json
os.environ["MODIN_ENGINE"] = "ray"  # or "dask"
open_ai_api_key = os.getenv("AIPROXY_KEY")
questions = pd.read_csv("sample_questions.csv")
from get_openai_embeddings import get_embeddings
from calculate_cosine_similarity import cosine_similarity
i = 0 
for question in questions.iterrows():
    embeddings = asyncio.run( get_embeddings(question[1]['Question']))

    if embeddings:
        embeddings_data = embeddings["data"][0]['embedding']
        # calculate the cosine similarity of embedding with the other embeddings present in the collection embeddings.json
        # load the collection
        with open("embeddings.json", "r") as file:
            collection = json.load(file)
        # use the cosine similarity function to calculate the similarity of the embedding with the other embeddings
        similarities = []
        for embedding in collection['embeddings']:
            similarity = cosine_similarity(embeddings_data, embedding['embedding'])
            similarities.append({
                "text": embedding['text'],
                "source": embedding['source'],
                "similarity": similarity
            })
        # sort the similarities in descending order
        similarities = sorted(similarities, key=lambda x: x['similarity'], reverse=True)
        # store question and its similarity in a file with the name as index of question
        with open(f"sample_questions_top_results/similarities_{i}.json", "w") as file:
            json.dump(similarities, file, indent=4)
        i += 1
    else:
            print("Failed to get embeddings.")