from typing import TypedDict,Annotated
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()
groq_api=os.getenv('groq_api')
llm=ChatGroq(model='gemma2-9b-it',api_key=groq_api)
from langgraph.graph import StateGraph,START,END
from langchain_core.messages import HumanMessage,SystemMessage,BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages

class ChatState(TypedDict):
    message:Annotated[list[BaseMessage],add_messages] 

def chat_node(state:ChatState):
    message=state['message']
    response=llm.invoke(message).content
    return {'message':response}
checkpointer=MemorySaver()
graph=StateGraph(ChatState)

graph.add_node('chat_node',chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

workflow=graph.compile(checkpointer=checkpointer)



