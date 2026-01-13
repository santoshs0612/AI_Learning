from openai import OpenAI
import requests
from dotenv import load_dotenv
import os 

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def get_weather(city:str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    else:
        return "Something wrong"
    return "Something went wrong"
    

def main():
    user_query = input("> ")
    response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role": "user",
            "content": user_query
        }
    ]
)
    print(f"🎁 {response.choices[0].message.content}")
    

# main()
print(get_weather("delhi"))

