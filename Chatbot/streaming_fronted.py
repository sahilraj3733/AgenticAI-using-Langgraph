import streamlit as st
from langraph_backend import workflow
from langchain_core.messages import HumanMessage
user_input=st.chat_input('Type here')



# st.session_state--dict butwhen we press enter it not start from first line it refresh when we mannuly refresh it
if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]


for mess in st.session_state['message_history']:
    with st.chat_message(mess['role']):
        st.write(mess['content'])

if(user_input):
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.write(user_input)

    ## interact with llm
    config={'configurable':{'thread_id':1}}
    result=workflow.stream({'message':HumanMessage(content=user_input)},config=config,stream_mode='messages') ## output message chunk and metadata


    #response=result['message'][-1].content


   
    with st.chat_message('ai'):
       ai_message= st.write_stream(
            message_chunk.content for message_chunk,meta_data in result
        )
    st.session_state['message_history'].append({'role':'ai','content':ai_message})