import streamlit as st
import numpy as np
import time
from resources.data import fixed_messages, topic_lists, interview_types
from api.llm import LLMManager
from api.audio import TTSManager, STTManager

# Initialize managers (you'll need to adapt these based on your specific implementations)
llm = LLMManager()
tts = TTSManager()
stt = STTManager()

st.title("Technical Interview Practice")

# Sidebar for interview settings
with st.sidebar:
    st.header("Interview Settings")
    interview_type = st.selectbox("Interview Type", options=interview_types, index=0)
    difficulty = st.selectbox("Difficulty", options=["Easy", "Medium", "Hard"], index=1)
    topic = st.selectbox("Topic", options=topic_lists[interview_type], index=0)
    requirements = st.text_area("Additional Requirements")
    terms_accepted = st.checkbox("I agree to the terms and conditions")
    start_btn = st.button("Generate Problem", disabled=not terms_accepted)

# Main area
if 'problem_generated' not in st.session_state:
    st.session_state.problem_generated = False

if start_btn and not st.session_state.problem_generated:
    st.session_state.problem_generated = True
    st.session_state.chat_history = []
    
    # Generate problem
    description = llm.get_problem(requirements, difficulty, topic, interview_type)
    st.session_state.description = description
    
    # Initialize chat
    st.session_state.chat_history = llm.init_bot(description, interview_type)

if st.session_state.problem_generated:
    st.header("Problem Statement")
    st.markdown(st.session_state.description)
    
    st.header("Solution")
    
    # Code/notes area
    if interview_type == "coding":
        code = st.code_editor("Write your code here", language="python", height=300)
    elif interview_type == "sql":
        code = st.code_editor("Write your query here", language="sql", height=300)
    else:
        code = st.text_area("Write your notes here", height=300)
    
    # Chat area
    st.header("Chat")
    for message in st.session_state.chat_history:
        st.chat_message(message['role']).write(message['content'])
    
    # User input
    user_input = st.chat_input("Your message")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        
        # Get AI response
        response = llm.get_text(st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)
    
    # End interview button
    if st.button("Finish Interview"):
        feedback = llm.end_interview(st.session_state.description, st.session_state.chat_history, interview_type)
        st.header("Feedback")
        st.markdown(feedback)
        st.session_state.problem_generated = False

# You'll need to implement audio handling separately, as Streamlit doesn't have built-in audio streaming like Gradio
