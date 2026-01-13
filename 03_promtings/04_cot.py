import json
from openai import OpenAI
from dotenv import load_dotenv
import os 

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)




SYSTEM_PROMPT = """
You are an expert AI Assistant in resolving user queries using chain of thought.
You work on START, PLAN and OUTPUT steps.
You need to first PLAN what needs to be done. The Plan can be multiple steps.
Once you think enough PLAN has been done, final can give OUTPUT.

Rules:
    - Strictily follow the JSON output format
    - Only run one tstep at a time.
    - The sequence of steps is START(where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to be displayed to the user).
Output JSON Format:
    {'steps': "START" | "PLAN" | "OUTPUT", "content": "string"}

Example:

Q: Hey Can you solve 2+ 3 * 5 /10
START: {"steps": "START", "content": "Seems like user is interestes in math problem"}
PLAN: {"steps": "PLAN", "content": "Looking at the problem, we should solve this using BODMAS method"}
PLAN: {"steps": "PLAN", "content": "First we must multiply 3 * 5 which  is 15"}
PLAN: {"steps": "PLAN", "content": "Now the new equation is 2 + 15/10"}
PLAN: {"steps": "PLAN", "content": "Now the new equation is 2 +1.5"}
PLAN: {"steps": "PLAN", "content": "Now finally let's perform the add 3.5"}
PLAN: {"steps": "PLAN", "content": "Great, We have solved and final ans is 3.5"}
OUTPUT: {"steps": "OUTPUT", "content": "Answer is 3.5"}





"""
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system","content": SYSTEM_PROMPT},
        {"role": "user", "content": "Can you write a code in python to add n numbers"},
        #Manually appending the respones getting by the assisten to get final output
        { "role": "assistant","content": json.dumps({"steps": "START", "content": "The user wants a Python function that can add 'n' numbers."})},
        { "role": "assistant","content": json.dumps({"steps": "PLAN", "content": "I need to write a Python function that can add a variable number of arguments. I will use `*args` to accept multiple numbers."})},
        { "role": "assistant","content": json.dumps({"steps": "PLAN", "content": "I will define a function called `add_numbers` that takes `*args` as an argument, allowing it to accept any number of positional arguments."})},
        { "role": "assistant","content": json.dumps({"steps": "PLAN", "content": "Inside the function, I will initialize a variable `total` to 0. Then, I will iterate through the `args` and add each number to the `total`."})},
        { "role": "assistant","content": json.dumps({"code": "def add_numbers(*args):\n    total = 0\n    for num in args:\n        total += num\n    return total\n\n# Example usage:\nprint(add_numbers(1, 2, 3))         # Output: 6\nprint(add_numbers(10, 20, 30, 40))  # Output: 100\nprint(add_numbers(5))               # Output: 5\nprint(add_numbers())                # Output: 0"})},
        { "role": "assistant","content": json.dumps({"steps": "OUTPUT", "content": "```python\ndef add_numbers(*args):\n    total = 0\n    for num in args:\n        total += num\n    return total\n\n# Example usage:\nprint(add_numbers(1, 2, 3))         # Output: 6\nprint(add_numbers(10, 20, 30, 40))  # Output: 100\nprint(add_numbers(5))               # Output: 5\nprint(add_numbers())                # Output: 0\n```\n\nThis Python function `add_numbers` uses `*args` to accept any number of positional arguments. It then iterates through these arguments, sums them up, and returns the total."})}
    ]
)

print(response.choices[0].message.content)

