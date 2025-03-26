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
        # Add space for the header
        st.markdown("<div style='height: 3rem;'>LRIGSCHAT</div>", unsafe_allow_html=True)
        
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
        st.subheader("Conversations")
        
        # Chat selection if multiple chats exist
        if "chat_sessions" not in st.session_state:
            st.session_state.chat_sessions = {"New Chat": []}
            st.session_state.current_chat = "New Chat"
            
        # Initialize chat titles if needed
        if "chat_titles" not in st.session_state:
            st.session_state.chat_titles = {}
        
        # Create a list of available chats
        chat_options = list(st.session_state.chat_sessions.keys())
        
        # Button to create a new chat - at the top for easier access
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("+ New", key="new_chat_btn"):
                # Create a new chat with a timestamp
                import time
                new_chat_name = f"Chat {time.strftime('%H:%M')}"
                st.session_state.chat_sessions[new_chat_name] = []
                st.session_state.current_chat = new_chat_name
                # Reset messages for the new chat
                st.session_state.messages = []
                st.rerun()
                
        with col2:
            # Rename current chat button
            if st.button("Rename", key="rename_chat_btn"):
                # Set a session state variable to indicate we want to rename
                st.session_state.show_rename_input = True
                st.rerun()
        
        # Display rename input if requested
        if st.session_state.get("show_rename_input", False):
            current_title = st.session_state.chat_titles.get(
                st.session_state.current_chat, 
                st.session_state.current_chat
            )
            new_title = st.text_input(
                "New title", 
                value=current_title,
                key="sidebar_rename_input"
            )
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Save", key="save_rename_btn"):
                    if new_title.strip():
                        # Rename chat
                        messages = st.session_state.chat_sessions[st.session_state.current_chat]
                        # Delete old chat
                        del st.session_state.chat_sessions[st.session_state.current_chat]
                        # Create new chat with renamed title
                        st.session_state.chat_sessions[new_title] = messages
                        st.session_state.current_chat = new_title
                        # Update chat title
                        st.session_state.chat_titles[new_title] = new_title
                        # Hide rename input
                        st.session_state.show_rename_input = False
                        st.rerun()
            
            with col2:
                if st.button("Cancel", key="cancel_rename_btn"):
                    st.session_state.show_rename_input = False
                    st.rerun()
        
        # Display divider
        st.divider()
        
        # Allow selection of existing chat
        for chat_name in chat_options:
            # Get chat title if available
            display_name = st.session_state.chat_titles.get(chat_name, chat_name)
            
            # Determine if this is the current chat
            is_current = chat_name == st.session_state.current_chat
            
            # Create columns for the chat name and delete button
            col1, col2 = st.columns([4, 1])
            
            with col1:
                # Create a button-like effect for each chat with conditional styling
                if st.button(
                    display_name, 
                    key=f"chat_{chat_name}",
                    use_container_width=True,
                    type="primary" if is_current else "secondary"
                ):
                    if not is_current:
                        st.session_state.current_chat = chat_name
                        # Update messages with the selected chat history
                        st.session_state.messages = st.session_state.chat_sessions[chat_name]
                        st.rerun()
            
            with col2:
                # Only show delete button if not current chat or if we have more than one chat
                if len(chat_options) > 1:
                    if st.button("🗑️", key=f"delete_{chat_name}"):
                        # Delete the chat
                        del st.session_state.chat_sessions[chat_name]
                        # If we deleted the current chat, switch to another chat
                        if chat_name == st.session_state.current_chat:
                            st.session_state.current_chat = list(st.session_state.chat_sessions.keys())[0]
                            st.session_state.messages = st.session_state.chat_sessions[st.session_state.current_chat]
                        st.rerun()
        
        
        # Information about the application
        with st.container():           
            # Minimal footer
            st.markdown("""<div style='position: fixed; bottom: 20px; left: 20px; font-size: 0.7em; opacity: 0.7;'>
                        Powered by Mistral AI <br>
                        LRIGSCHAT - © 2025
                        </div>""", unsafe_allow_html=True)
    
    return config["default_model"], st.session_state.api_status 