from fastapi import FastAPI, Body
from ollama import Client

app = FastAPI()

client = Client(
    host = "http://localhost:11434",
)
@app.get("/")
def read_root():
    return {"Hello :" "Lord"}


@app.get("/contact-us")
def read_root():
    return {"Email :" "Lord@rings.com"}

@app.post("/chat")
def chat(
        message: str = Body(..., description= "The Message")
):
    response = client.chat(model="gemma3:270m", messages= [
        { "role": "user", "content" : message}
    ])
    return {"response": response.message.content}

# Ollama running with gemma4:270m in docker @11434