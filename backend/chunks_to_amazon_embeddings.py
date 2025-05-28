# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx",
#    "python-dotenv",
# ]
# ///

import asyncio
from get_amazon_embeddings import get_embeddings
import json
with open("chunks.json", "r") as file:
    lines = file.readlines()
# create a collection for storing embeddings and text 
collection = {
    "name":"documents-embeddings",
    "embeddings":[]
}
for line in lines:
    line = line.strip()
    if line:
        # load line as a json object
        
        line = json.loads(line)
        print(f"Processing chunk: {line}")
        embeddings = asyncio.run( get_embeddings(line['content']))
        if embeddings:
            embeddings_data = embeddings["response"]["embedding"]
            # add the embeddings and text to the collection
            collection['embeddings'].append({
                "text": line['content'],
                "source":line['id'],
                "embedding": embeddings_data
            })
        else:
            print("Failed to get embeddings.")

# save the collection to a file
with open("embeddings_amazon.json", "w") as file:
    import json
    json.dump(collection, file, indent=4)