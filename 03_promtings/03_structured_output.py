
from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyBxfNfumG2MWtl8njFRRMML8ALd-JK_6VQ",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)




SYSTEM_PROMPT = """
You are an expert in Coding and you only ans Coding related questions, if question is not related to the coding then do not provide the answers give sorry 

Output Format:
{{
"code": "string" or null,
"isCodingQuestion": boolean
}}
Examples:
Q: Can you explain the (a + b)^2.
A: {{
"code": null,
"isCodingQuestion": flase
}}

Q: Write asimple Python program to add two numbers?
A: {{
"code": "def add(a, b):
        return a + b",
"isCodingQuestion": true
}}d
        


"""
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[

        {"role": "system",
         "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "Can you write a code in cPP saying hello to the programer"
        }
    ]
)

print(response.choices[0].message.content)

