from typing import TypedDict, Annotated 
from langgraph.graph import StateGraph, START, END
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load API key for the LLM
load_dotenv()
my_api_key = os.getenv("GOOGLE_API_KEY")

# Instantiate the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=my_api_key
)

# Create state schema (Annotated list and add_messages reducer)
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):
    messages = state["messages"]  
    response = llm.invoke(messages)
    return {"messages": [response]}


# Build the Graph
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# Compile the Graph
chatbot = graph.compile()