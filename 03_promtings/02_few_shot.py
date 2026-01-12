# Few Shot Promptings : The is basically asking after providing the some examples to the system prompts to the ai

from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyBxfNfumG2MWtl8njFRRMML8ALd-JK_6VQ",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)



#Few Shot Prompting: Directily giving the inst to the model and few examples to the model

SYSTEM_PROMPT = """
You are an expert in Coding and you only ans Coding related questions, if question is not related to the coding then do not provide the answers give sorry 
Examples:
Q: Can you explain the (a + b)^2.
A: Sorry ,I can only help you with the coding related quations.

Q: Write asimple Python program to add two numbers?
A: `def add(a, b):
        return a + b
        `


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

#1. Few-shot Prompting: The model is provided with a few examples before asking it to generate the response.