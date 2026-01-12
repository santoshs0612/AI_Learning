from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START,END

# State

class State(TypedDict):
    messages: Annotated[list,add_messages]

# Node
def chatbot(state: State):
    print("\n\n Inside chatbot node", state)
    return {"messages": ["Hi This is a message ffrom ChatBot Node"]}

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

updated_state = graph.invoke(State({"messages": ["Hi, My name is Santosh Kumar"]}))
print("\n\nupdated_state", updated_state)

# (START)-->chatbot--->samplenode--->(END)
