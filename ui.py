import streamlit as st
from agent import run_it_agent

# Browser tab settings
st.set_page_config(
    page_title="Autonomous IT Service Desk Agent", page_icon="🤖", layout="centered")

# Title and instructions
st.title("🤖 Autonomous IT Service Desk Agent")
st.markdown("Your AI-powered assistant for querying enterprise systems, checking permissions, tracking service health, and logging tickets.")

# Creates a list called 'messages' if it doesn't yet exist, which keeps all chat history while the browser window is open. Otherwise, this code is ignored.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous chat history (role name and query/response) between the user and Gemini when the app reruns
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 'st.chat_input' renders a chat box for the user to type in their query. ':=' assigns the query text to 'prompt' and also checks to see if text was actually entered at the same time' 
if prompt := st.chat_input("How can I help you with IT support today?"):
    # Add a new dictionary item to the 'messages' list for the user's query. Display a chat bubble on screen and populate it with the user's query
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display Gemini's response
    with st.chat_message("assistant"):
        with st.spinner("Processing request..."):
            try:
                # Run the core agent loop called run_it_agent in agent.py
                response_text = run_it_agent(prompt)
                st.markdown(response_text)
                
                # Save Gemini's response and sources to the history (the 'messages' list) so that it can be displayed again after the next query
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                error_message = f"⚠️ Error connecting to agent backend: {str(e)}"
                st.error(error_message)