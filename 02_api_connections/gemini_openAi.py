from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyBxfNfumG2MWtl8njFRRMML8ALd-JK_6VQ",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[

        {"role": "system",
         "content": "You are an expert in Maths and you only ans maths related questions, if question is not related to the mathematics then do not provide the answers give sorry "
         },
        {
            "role": "user",
            "content": "Hey can you solve me this (a+b)^2"
        }
    ]
)

print(response.choices[0].message.content)