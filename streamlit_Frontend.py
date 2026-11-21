import streamlit as st
from langgraph_backend import chatbot , retireve_all_threads , delete_thread
from langchain_core.messages import HumanMessage
import uuid

# ********** UTILITY FUNCTION *************
def generate_thread_id():
    thread_id = uuid.uuid4()
    return str(thread_id)

def reset_chat():
    st.session_state['thread_id'] = generate_thread_id()
    st.session_state['message_history'] = []
    
def add_thread_id(thread_id, title):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)
    st.session_state['thread_titles'][thread_id] = title
    
def get_thread_title(thread_id):
    # Pehle cache check karo
    if thread_id in st.session_state['thread_titles']:
        return st.session_state['thread_titles'][thread_id]

    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    messages = state.values.get('messages', [])

    title = 'New Chat'
    for msg in messages:
        if isinstance(msg, HumanMessage):
            content = msg.content
            if isinstance(content, list):
                content = ''.join(b.get('text', '') for b in content if isinstance(b, dict))
            title = content[:30]
            break

    st.session_state['thread_titles'][thread_id] = title
    return title

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get('messages', [])

def delete_chat(thread_id):
    delete_thread(thread_id)

    if thread_id in st.session_state['chat_threads']:
        st.session_state['chat_threads'].remove(thread_id)
    st.session_state['thread_titles'].pop(thread_id, None)

    # Agar wahi chat khuli hui thi to screen bhi khali kar do
    if st.session_state['thread_id'] == thread_id:
        reset_chat()

# *************** Session Setup *************** 
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
    
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'thread_titles' not in st.session_state:
    st.session_state['thread_titles'] = {}

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retireve_all_threads()

# add_thread_id(st.session_state['thread_id'], "New Chat")
    
# *************** SideBar UI *************** 
st.sidebar.title("Langraph ChatBot")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Conversation")

for thread_id in st.session_state['chat_threads'][::-1]:

    title = get_thread_title(thread_id)

    col1, col2 = st.sidebar.columns([5, 1])

    if col1.button(title, key=f"open_{thread_id}"):

        st.session_state['thread_id'] = thread_id

        messages = load_conversation(thread_id)
        temp_messages = []

        for msg in messages:
            role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
            content = msg.content

            if isinstance(content, list):
                content = ''.join(
                    block['text']
                    for block in content
                    if block.get('type') == 'text'
                )

            temp_messages.append({'role': role, 'content': content})

        st.session_state['message_history'] = temp_messages
        st.rerun()

    if col2.button("", key=f"del_{thread_id}", icon=":material/delete:", help="Delete chat"):
        delete_chat(thread_id)
        st.rerun()

# Main UI
# Loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])
    
user_input = st.chat_input('Type here')

if user_input:
    
    # Generate chat title from first user message
    if not st.session_state['message_history']:
        title = user_input[:30]
        add_thread_id(st.session_state['thread_id'], title)
        
    # First add message in History
    st.session_state['message_history'].append({'role':'user' , 'content' : user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    CONFIG = {'configurable': {'thread_id' : st.session_state['thread_id']}}
    # First add message in History 
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            block['text'] 
            for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                    config=CONFIG,
                    stream_mode='messages'
            )
            if isinstance(message_chunk.content, list)
            for block in message_chunk.content
            if block.get('type') == 'text'
        )
    
    st.session_state['message_history'].append({'role':'assistant' , 'content' : ai_message})
    st.rerun()