import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8008")

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Chatbot")
st.markdown("---")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Chat input
st.markdown("---")
user_input = st.chat_input("Ask me something...", key="chat_input")

if user_input:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    # Get AI response
    try:
        with st.spinner("🤔 Thinking..."):
            response = requests.post(
                f"{API_URL}/ask",
                json={"text": user_input},
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("answer", "Sorry, I couldn't generate a response.")
            else:
                ai_response = f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.ConnectionError:
        ai_response = f"❌ Cannot connect to API at {API_URL}. Is the FastAPI server running?"
    except requests.exceptions.Timeout:
        ai_response = "⏱️ Request timeout. The server is taking too long to respond."
    except Exception as e:
        ai_response = f"❌ Error: {str(e)}"

    # Add AI response to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response
    })

    # Display AI response
    with st.chat_message("assistant"):
        st.write(ai_response)

# Sidebar
with st.sidebar:
    st.header("ℹ️ Info")
    st.write(f"**API URL:** {API_URL}")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("""
    ### How it works:
    1. Type your question
    2. Click Enter or the send button
    3. Wait for the AI response

    This chatbot connects to a FastAPI backend.
    """)
