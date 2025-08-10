from typing import TypedDict,Annotated,Optional
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()
groq_api=os.getenv('groq_api')
llm=ChatGroq(model='gemma2-9b-it',api_key=groq_api)
from langgraph.graph import StateGraph,START,END
from langchain_core.messages import HumanMessage,AIMessage,BaseMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
import sqlite3

class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages] 
   



def chat_node(state:ChatState):
    message=state['messages']
    response=llm.invoke(message)
    return {'messages':[response]}
## db connect
db=sqlite3.connect(database='chatbot.db',check_same_thread=False)
checkpointer=SqliteSaver(conn=db)

## graph define
graph=StateGraph(ChatState)

graph.add_node('chat_node',chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

workflow=graph.compile(checkpointer=checkpointer)

# cnf={'configurable':{'thread_id':'thread-1'}}
# output=workflow.invoke(
#         {'messages':[HumanMessage(content='what is capital of bihar?')]},
#         config=cnf
# )
# print(workflow.get_state(config=cnf))

def get_all_thread():

    all_thread=set()

    for checpoint in checkpointer.list(None):
        all_thread.add(checpoint.config['configurable']['thread_id'])
    return list(all_thread)

# print(workflow.get_state(config=cnf))


