# Zero Shot Promptings : The is basically asking directilly prompts to the ai

from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyBxfNfumG2MWtl8njFRRMML8ALd-JK_6VQ",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)




SYSTEM_PROMPT = "You are an expert in Coding and you only ans Coding related questions, if question is not related to the coding then do not provide the answers give sorry "
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[

        {"role": "system",
         "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "Can you tell me the joke"
        }
    ]
)

print(response.choices[0].message.content)

#1. Zero-shot Prompting: The model is given a direct question or task without prior examples