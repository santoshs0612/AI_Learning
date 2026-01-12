from mem0 import Memory
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
neo_url = os.getenv("NEO_CONNECTION_URI")
neo_username = os.getenv("NEO_USERNAME")
neo_password = os.getenv("NEO_PASSWORD")
client = OpenAI(
    api_key= api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
config = {
    "version": "v1.1",
    "embedder": {
        "provider" : "gemini",
        "config": {"api_key": api_key, "model": "models/text-embedding-004",}
    },
    "llm": {
        "provider" : "gemini",
        "config": {"api_key": api_key, "model": "gemini-2.5-flash"}        
    },
    "graph_store":{
        "provider": "neo4j",
        "config": {
            "url": neo_url,
            "username": neo_username,
            "password": neo_password

        }
    },
    "vector_store":{
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
            "collection_name": "gemini_memories",
            "embedding_model_dims": 768 
        }
    }
}


mem_client = Memory.from_config(config)

while True:

    user_query  = input("> ")


    search_memory = mem_client.search(query=user_query, user_id="santosh")
    memories = [
        f"ID: {mem.get("id")}\n Memory: {mem.get("memory")} " 
        for mem in search_memory.get("results")
    ]

    print("Found Memories", memories)

    SYSTEM_PROMPT = f"""Here is the context about the user: {json.dumps(memories)}
    """

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system","content": SYSTEM_PROMPT},
            {"role": "user","content": user_query}
        ]
    )

    ai_response = response.choices[0].message.content

    print("AI: ", ai_response)

    mem_client.add(
        user_id= "santosh",
        messages=[
            {"role": "user","content": user_query},
            {"role": "assistant","content": ai_response},

        ]
    )

    print("Memory has been updated ")

# rate excedded need to check again