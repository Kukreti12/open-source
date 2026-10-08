import gradio as gr
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8008")

def chat(user_message, history):
    """Send message to FastAPI backend and get response"""
    try:
        # Send POST request to FastAPI
        response = requests.post(
            f"{API_URL}/ask",
            json={"text": user_message},
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

    # Return just the AI response (ChatInterface manages history)
    return ai_response


# Create Gradio interface
demo = gr.ChatInterface(
    chat,
    examples=["What is AI?", "Hello", "Tell me a joke"],
    title="AI Chatbot",
    description=f"Chat with the AI assistant (Connected to: {API_URL})"
)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
