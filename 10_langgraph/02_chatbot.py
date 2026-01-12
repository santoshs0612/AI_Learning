from dotenv import load_dotenv
import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START,END
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

llm = init_chat_model(
    "gemini-2.5-flash", 
    model_provider="google_genai",
    temperature=0
)

# State

class State(TypedDict):
    messages: Annotated[list,add_messages]

# Node
def chatbot(state: State):
    print("\n\n Inside chatbot node", state)
    response = llm.invoke(state.get("messages"))
    return {"messages": [response]}

def samplenode(state: State):
    print("\n\n Inside samplenode node", state)
    return {"messages": ["Sample Message Appended"]}


# Builder creating a graph
graph_builder = StateGraph(State)


# Add nodes to graph 

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("samplenode",samplenode)

# Adding edges to the nodes (connecting them)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","samplenode")
graph_builder.add_edge("samplenode",END)

# Final graph ready 
graph = graph_builder.compile()


# Invoking

# updated_state = graph.invoke(State({"messages": ["Hi, My name is Santosh Kumar"]}))
initial_input = {"messages": [HumanMessage(content="Hi, My name is Santosh Kumar")]}
updated_state = graph.invoke(initial_input)

# print("\n\nupdated_state", updated_state)
print("\nFinal State Messages:")
for msg in updated_state["messages"]:
    print(f"{type(msg).__name__}: {msg.content}")
# (START)-->chatbot--->samplenode--->(END)
