import sqlite3
import os
from langgraph.graph import StateGraph , START , END
from typing import TypedDict , Annotated
from langchain_core.messages import BaseMessage , HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-3.5-flash-lite",
    max_tokens = 512,
)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    
def chat_node(state: ChatState) -> ChatState:
    
    messages = state['messages']
    response = llm.invoke(messages)
    
    return {'messages': [response]}

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chatbot.db')
conn = sqlite3.connect(database=DB_PATH, check_same_thread=False)
# checkpointer
checkpointer = SqliteSaver(conn = conn)

graph = StateGraph(ChatState)

# node
graph.add_node('chat_node', chat_node)

# Edges
graph.add_edge(START , 'chat_node')
graph.add_edge('chat_node' , END)

chatbot = graph.compile(checkpointer=checkpointer)

def retireve_all_threads():
    seen = []
    for checkpoint in checkpointer.list(None):   # newest pehle
        tid = checkpoint.config['configurable']['thread_id']
        if tid not in seen:
            seen.append(tid)
    return seen[::-1]

def delete_thread(thread_id):
    checkpointer.delete_thread(thread_id)