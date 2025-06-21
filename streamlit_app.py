import streamlit as st
import requests
import json
from typing import List, Dict
import sys
import os

# -- Path setup for imports --
# Add the project root to the path to allow absolute imports from 'backend'
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from backend.app import qa
from backend.app import semantic_search

# Configuration
# BACKEND_URL = "http://localhost:8000" # No longer needed

def init_session_state():
    """Initialize session state for chat history"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "api_key_set" not in st.session_state:
        st.session_state.api_key_set = False

def main():
    st.set_page_config(
        page_title="Sixt Rental Q&A Chatbot",
        page_icon="🚗",
        layout="wide"
    )
    
    # Initialize session state and load the model at startup
    init_session_state()
    semantic_search.get_model() # This will pre-load the sentence transformer model
    
    # Header
    st.title("🚗 Sixt Rental Q&A Chatbot")
    st.markdown("Ask questions about Sixt car rental terms and conditions")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Check for Google API Key
        api_key_set = bool(os.getenv("GOOGLE_API_KEY"))
        if api_key_set:
            st.success("✅ Google API Key is set")
        else:
            st.error("❌ Google API Key not set")
            st.info("Please set the GOOGLE_API_KEY environment variable to run the chatbot.")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    # Main chat interface
    st.info("This is a demo chatbot. For official information, please visit the Sixt website.")

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about Sixt rental terms..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            if not api_key_set:
                st.error("Cannot process request: GOOGLE_API_KEY is not set.")
                return

            with st.spinner("🤖 Searching terms and thinking..."):
                try:
                    response = qa.answer_question(prompt) # Call the local function directly
                    
                    answer = response.get("answer", "Sorry, I couldn't find an answer.")
                    st.markdown(answer)
                    
                    # Show source count
                    if response.get("sources") and len(response["sources"]) > 0:
                        st.info(f"📚 Based on {len(response['sources'])} relevant section(s) from the rental terms.")
                    
                    # Add assistant message to chat history
                    st.session_state.messages.append({"role": "assistant", "content": answer})

                except Exception as e:
                    error_msg = f"❌ An error occurred: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main() 