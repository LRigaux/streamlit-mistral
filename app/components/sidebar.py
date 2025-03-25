"""
Sidebar component for the Streamlit app.
Displays chat management options and app information.
"""
import streamlit as st
import logging
from app.utils.mistral_client import test_api_connection
from app.config.config import load_config

logger = logging.getLogger(__name__)

def create_sidebar():
    """
    Create and render the application sidebar.
    
    Returns:
        bool: API status
    """
    with st.sidebar:
        st.title("Mistral Chat")
        
        # Load configuration
        config = load_config()
        
        # Silent API check on startup
        if "api_status_checked" not in st.session_state:
            st.session_state.api_status_checked = False
            st.session_state.api_status = None
            
            try:
                logger.info("Testing API connection on startup")
                api_status = test_api_connection()
                st.session_state.api_status = api_status
                st.session_state.api_status_checked = True
                logger.info(f"API connection test result: {api_status}")
            except Exception as e:
                logger.error(f"API connection error: {str(e)}")
                st.session_state.api_status = False
                st.session_state.api_status_checked = True
        
        # Chat management
        st.header("Chat Management")
        
        # Chat selection if multiple chats exist
        if "chat_sessions" not in st.session_state:
            st.session_state.chat_sessions = {"New Chat": []}
            st.session_state.current_chat = "New Chat"
            
        # Create a list of available chats
        chat_options = list(st.session_state.chat_sessions.keys())
        
        # Allow selection of existing chat
        selected_chat = st.selectbox(
            "Select Chat",
            options=chat_options,
            index=chat_options.index(st.session_state.current_chat)
        )
        
        # Update current chat if changed
        if selected_chat != st.session_state.current_chat:
            st.session_state.current_chat = selected_chat
            # Update messages with the selected chat history
            st.session_state.messages = st.session_state.chat_sessions[selected_chat]
            st.rerun()
            
        # Button to create a new chat
        if st.button("New Chat"):
            # Create a new chat with a timestamp
            import time
            new_chat_name = f"Chat {time.strftime('%H:%M:%S')}"
            st.session_state.chat_sessions[new_chat_name] = []
            st.session_state.current_chat = new_chat_name
            st.session_state.messages = []
            st.rerun()
        
        # Delete current chat button
        if len(chat_options) > 1 and st.button("Delete Current Chat"):
            del st.session_state.chat_sessions[st.session_state.current_chat]
            st.session_state.current_chat = list(st.session_state.chat_sessions.keys())[0]
            st.session_state.messages = st.session_state.chat_sessions[st.session_state.current_chat]
            st.rerun()
        
        # Information about the application
        st.header("About")
        st.markdown("""
        This application uses Mistral AI's models to provide chat and image analysis capabilities.
        
        #### Features:
        - Multi-modal chat with image analysis
        - Multiple chat sessions
        - Beautiful autumn-inspired theme
        """)
        
        # Footer
        st.markdown("---")
        st.caption("Mistral AI Chat App © 2025")
    
    return config["default_model"], st.session_state.api_status 