from openai import OpenAI
import requests
import json
from dotenv import load_dotenv
import os 

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
# Initialize OpenAI client with Gemini endpoint
client = OpenAI(
    api_key=api_key,  # Use your Gemini API key
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def get_weather(city:str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    else:
        return "Something wrong"

# Add this helper function before your loop
def extract_first_json(text):
    """
    Extracts the first valid JSON object from a string that might contain
    multiple concatenated JSON objects or extra text.
    """
    try:
        # Try parsing directly first
        return json.loads(text)
    except json.JSONDecodeError as e:
        # If "Extra data" error, it means we have valid JSON followed by more stuff.
        # e.pos contains the character index where parsing stopped (end of first JSON)
        if e.msg.startswith("Extra data"):
            return json.loads(text[:e.pos])
        # If it's a different error, try finding the first '{' and matching '}'
        # This is a fallback for messy LLM output
        try:
            start_idx = text.find('{')
            if start_idx == -1: return None
            
            # Simple brace counting to find end of object
            balance = 0
            for i in range(start_idx, len(text)):
                if text[i] == '{': balance += 1
                elif text[i] == '}': balance -= 1
                
                if balance == 0:
                    return json.loads(text[start_idx:i+1])
        except:
            pass
        return None


available_tools = {
    "get_weather" : get_weather
}



print (" ")
print (" ")
print (" ")
print (" ")

SYSTEM_PROMPT = """
You are an expert AI Assistant in resolving user queries using chain of thought.
You work on START, PLAN and OUTPUT steps.
You need to first PLAN what needs to be done. The Plan can be multiple steps.
Once you think enough PLAN has been done, final can give OUTPUT.
You can also call a tool if required from the list os available tools.
for every tool call wait for the observer step which is the output from the tool.

Rules:
    - Strictily follow the JSON output format
    - Only run one step at a time.
    - The sequence of steps is START(where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to be displayed to the user).
Output JSON Format: strictilly follow this instructions
    {'step': "START" | "PLAN" | "OUTPUT" | "TOOL", "content": "string"}
Available Tools:
    - get_weather: Takes city name as an input string and returns the weather info about the city.

Example 1:

Q: Hey Can you solve 2+ 3 * 5 /10
START: {"step": "START", "content": "Seems like user is interested in math problem"}
PLAN: {"step": "PLAN", "content": "Looking at the problem, we should solve this using BODMAS method"}
PLAN: {"step": "PLAN", "content": "First we must multiply 3 * 5 which is 15"}
PLAN: {"step": "PLAN", "content": "Now the new equation is 2 + 15/10"}
PLAN: {"step": "PLAN", "content": "Now the new equation is 2 +1.5"}
PLAN: {"step": "PLAN", "content": "Now finally let's perform the add 3.5"}
PLAN: {"step": "PLAN", "content": "Great, We have solved and final ans is 3.5"}
OUTPUT: {"step": "OUTPUT", "content": "Answer is 3.5"}

Example 2:

Q: What is the weather of Delhi?
START: {"step": "START", "content": "Seems like user is looking for a weather report of delhi india"}
PLAN: {"step": "PLAN", "content": "Let's see if we have any available tool from the list of available tools"}
PLAN: {"step": "PLAN", "content": "Great, We have get_weather tool available for this query."}
PLAN: {"step": "PLAN", "content": "Now I have to call get_weather tool having delhi as input for city "}
TOOL: {"step": "TOOL", "tool": "get_weather","input": "delhi"}
OBSERVE: {"step": "OBSERVE", "tool": "get_weather","output": "The temperature of delhi is hazy with 19 deg C"}
PLAN: {"step": "PLAN", "content": "Great, We have a weather info about delhi"}
OUTPUT: {"step": "OUTPUT", "content": "The temperature of delhi is hazy with 19 deg C"}

"""

message_history = [{"role": "system", "content": SYSTEM_PROMPT}]

user_query = input("👉 ")
message_history.append({"role": "user", "content": user_query})

while True:
    response = client.chat.completions.create(
        model="gemini-2.5-flash",  # Use Gemini model
        response_format={"type": "json_object"},
        messages=message_history
    )
    
    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})
    try:
        parsed_result = json.loads(raw_result)  # Fixed: json.loads instead of json.load
    except json.JSONDecodeError:
        parsed_result = extract_first_json(raw_result)  # Fixed: json.loads instead of json.load

    if not parsed_result:
        print("❌ Failed to parse JSON from model response:", raw_result)
        continue

    
    if  isinstance(parsed_result,list):
        if len(parsed_result) > 0:
            parsed_result = parsed_result[0]
        else:
            continue
    step = parsed_result.get("step")
    content = parsed_result.get("content")
    if step == "START":
        print("🔥", parsed_result.get("content"))
        continue
    elif step == "PLAN":
        print("🧠 ", parsed_result.get("content"))
        continue
    elif step == "TOOL":
        tool_to_call = parsed_result.get("tool")
        tool_input = parsed_result.get("input")
        print(f"🔨: Calling: {tool_to_call} Input: {tool_input}")
        tool_response = available_tools[tool_to_call](tool_input)
        print(f"🔨: Called: {tool_to_call} Input: {tool_input} response is {tool_response}")
        message_history.append({"role": "user", "content": json.dumps({"step": "OBSERVE", "tool":tool_to_call, "input": tool_input, "output":tool_response})})
        continue
    elif step == "OUTPUT":
        print("🎁", parsed_result.get("content"))
        break

print ("")
print ("")
print ("")
print ("")
