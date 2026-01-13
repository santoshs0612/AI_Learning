from dotenv import load_dotenv
from openai import OpenAI
from dotenv import load_dotenv
import os 

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[

        {"role": "user",
         "content": [
             {"type": "text", "text" : "Generate a caption for this image in about one line"},
             { "type":"image_url", "image_url": {"url": "https://images.pexels.com/photos/879109/pexels-photo-879109.jpeg"}}
         ]
         },
    ]
)

print(response.choices[0].message.content)