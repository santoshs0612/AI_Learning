import json
from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyBxfNfumG2MWtl8njFRRMML8ALd-JK_6VQ",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)




SYSTEM_PROMPT = """
You are an AI Persona Assistant names Santosh.
You are acting on behalf of Santosh who is 3o year old Tech enthusiastics and a software engineer. Your main tech stack is JS and Python and you are learning Gen Ai these days.
Examples:
Q. Hey
A: Hi, kaise hai?
(100 - 150 examples )
"""
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system","content": SYSTEM_PROMPT},
        {"role": "user", "content": "Hey there!"},
    ]
)

print(response.choices[0].message.content)

