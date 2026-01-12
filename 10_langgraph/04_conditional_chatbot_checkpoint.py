from dotenv import load_dotenv
import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START,END
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.mongodb import MongoDBSaver


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



# Builder creating a graph
graph_builder = StateGraph(State)


# Add nodes to graph 

graph_builder.add_node("chatbot",chatbot)

# Adding edges to the nodes (connecting them)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot",END)

# Final graph ready 
graph = graph_builder.compile()

def compile_graph_with_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)


DB_URI = "mongodb://admin:admin@localhost:27017"
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_with_checkpointer =  compile_graph_with_checkpointer(checkpointer)

    config = {
        "configurable":{
            "thread_id":"santosh" # change thread  for new identity
        }
    }


    for chunk in graph_with_checkpointer.stream(
        State({"messages": ["What was my name?"]}), config, stream_mode="values"
    ):
        chunk["messages"][-1].pretty_print()
    # Invoking

    # updated_state = graph.invoke(State({"messages": ["Hi, My name is Santosh Kumar"]}),config)
    # updated_state = graph.invoke(State({"messages": ["What is my namme?"]}), config)
    # initial_input = {"messages": [HumanMessage(content="Hi, My name is Santosh Kumar")], }
    # updated_state = graph.invoke(initial_input)

    # print("\n\nupdated_state", updated_state)
    # print("\nFinal State Messages:")
    # for msg in updated_state["messages"]:
    #     print(f"{type(msg).__name__}: {msg.content}")


# (START)-->chatbot--->(END)
# state = {message; ["hey there"]}
# node runs: chatbot(state: ["Hey there"]) --> ["Hi this is a message form chatBot node"]

# Checkpointer (santosh) = Hey , My same is santosh kumar