import streamlit as st
from langgraph_db_backend import workflow,get_all_thread
from langchain_core.messages import HumanMessage
import uuid


# ************************ Utilty function' *****************
def generate_thread_id():
    thread_id=uuid.uuid4()
    return thread_id

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_thread']:
        st.session_state['chat_thread'].append(thread_id)

def reset_chat():
    thread_id=generate_thread_id()
    st.session_state['thread_id']=thread_id
    add_thread(thread_id)
    st.session_state['message_history']=[]

def load_conversation(thread_id):
    state = workflow.get_state(config={'configurable': {'thread_id': thread_id}})
    # st.sidebar.write("Debug: Loaded state", state.values)  
    return state.values.get('messages', [])


# **************************************** Session Setup *****************************

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_thread' not in st.session_state:
    st.session_state['chat_thread']=get_all_thread()
    
add_thread(st.session_state['thread_id'])





#******************* Sidebar**************

st.sidebar.title('Langgraph Chatbot')
if st.sidebar.button('New Chat'):
    reset_chat()
st.sidebar.title('My Conversation')
for thd_id in st.session_state['chat_thread'][::-1]:
    if st.sidebar.button(str(thd_id)):
        st.session_state['thread_id']=thd_id
        messages=load_conversation(thd_id)

        temp_message=[]
        for msg in messages:
            if isinstance(msg,HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_message.append({'role':role,'content':msg.content})
        st.session_state['message_history']=temp_message



# ************************* Main UI *************************

user_input=st.chat_input('Type here')
for mess in st.session_state['message_history']:
    with st.chat_message(mess['role']):
        st.write(mess['content'])

if(user_input):
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.write(user_input)

    ## interact with llm
    config={'configurable':{'thread_id':st.session_state['thread_id']}}
    result=workflow.stream({'messages':HumanMessage(content=user_input)},config=config,stream_mode='messages') ## output message chunk and metadata


    #response=result['message'][-1].content
   
    with st.chat_message('ai'):
       ai_message= st.write_stream(
            message_chunk.content for message_chunk,meta_data in result
        )
    st.session_state['message_history'].append({'role':'ai','content':ai_message})