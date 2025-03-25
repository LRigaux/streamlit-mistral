"""
Sidebar component for the Streamlit app.
Displays chat management options and app information.
"""
import streamlit as st
import logging
from typing import Tuple, Dict, List, Any
from app.utils.mistral_client import test_api_connection
from app.config.config import load_config
from app.state.session_state import (
    get_all_chats, 
    get_chat_display_name, 
    create_new_chat, 
    switch_to_chat, 
    delete_chat, 
    rename_chat
)

logger = logging.getLogger(__name__)

def create_sidebar() -> Tuple[str, bool]:
    """
    Create and render the application sidebar.
    
    Returns:
        Tuple containing:
        - default_model (str): The default model to use
        - api_status (bool): True if API connection is successful, False otherwise
    """
    with st.sidebar:
        # Add space for the header
        st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)
        
        st.title("LRIGSCHAT")
        
        # Load configuration
        config = load_config()
        
        # Silent API check on startup
        api_status = _check_api_connection()
        
        # Chat management
        _render_chat_management()
        
        # Display a divider and app information at the bottom
        st.divider()
        
        # Information about the application
        _render_app_info()
    
    return config["default_model"], api_status

def _check_api_connection() -> bool:
    """
    Check the API connection and store the result in session state.
    
    Returns:
        True if connection is successful, False otherwise
    """
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
    
    return st.session_state.api_status

def _render_chat_management():
    """Render the chat management section of the sidebar."""
    st.subheader("Conversations")
    
    # Create a list of available chats
    chat_options = list(get_all_chats().keys())
    
    # Button to create a new chat - at the top for easier access
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("+ New", key="new_chat_btn"):
            create_new_chat()
            st.rerun()
            
    with col2:
        # Rename current chat button
        if st.button("Rename", key="rename_chat_btn"):
            # Set a session state variable to indicate we want to rename
            st.session_state.show_rename_input = True
            st.rerun()
    
    # Display rename input if requested
    if st.session_state.get("show_rename_input", False):
        current_chat = st.session_state.current_chat
        current_title = get_chat_display_name(current_chat)
        
        new_title = st.text_input(
            "New title", 
            value=current_title,
            key="sidebar_rename_input"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Save", key="save_rename_btn"):
                if new_title.strip():
                    rename_chat(current_chat, new_title)
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
        display_name = get_chat_display_name(chat_name)
        
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
                    switch_to_chat(chat_name)
                    st.rerun()
        
        with col2:
            # Only show delete button if not current chat or if we have more than one chat
            if len(chat_options) > 1:
                if st.button("🗑️", key=f"delete_{chat_name}"):
                    delete_chat(chat_name)
                    st.rerun()

def _render_app_info():
    """Render the application information section."""
    with st.container():
        st.caption("""
        Powered by Mistral AI
        
        This application uses Mistral AI's multimodal models for chat and image analysis.
        """)
        
        # Minimal footer
        st.markdown("<div style='position: fixed; bottom: 20px; left: 20px; font-size: 0.7em; opacity: 0.7;'>LRIGSCHAT - © 2025</div>", unsafe_allow_html=True) 