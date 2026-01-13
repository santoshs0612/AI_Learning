import json
from google import genai
from dotenv import load_dotenv
import os 

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(
    api_key= api_key
)

# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents="Explain how AI works in a few words",
# )

# print(response.text)

# client = OpenAI(
#     api_key="AIzaSyBxfNfumG2MWtl8njFRRMML8ALd-JK_6VQ",
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )


print (" ")
print (" ")
print (" ")
print (" ")

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

message_history = [{"role": "system", "content": SYSTEM_PROMPT}]

user_query = input("🎬 " )
message_history.append({"roles": "user", "content": user_query})


while True:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        response_format={"type": "json_object"},
        messages = message_history
    )

    raw_result = (response.choices[0].message.content)
    message_history.append({"role": "assistant", "content": raw_result})
    parsed_result = json.load(raw_result)
    
    if parsed_result.get("step") == "START":
        print("🔥", parsed_result.get("content"))
        continue
    elif parsed_result.get("step") == "PLAN":
        print("🧠 ", parsed_result.get("content"))
        continue
    elif parsed_result.get("step") == "OUTPUT":
        print("🎁",parsed_result.get("content"))
        break


print ("")
print ("")
print ("")
print ("")