"""
Session state management for the Streamlit application.
Handles initialization and management of session state variables.
"""
from typing import Dict, List, Any, Optional
import streamlit as st
import logging
import time

logger = logging.getLogger(__name__)

def initialize_session_state():
    """
    Initialize all session state variables needed for the application.
    This function should be called at the start of the application to ensure
    all required state variables are properly set up.
    """
    logger.debug("Initializing session state")
    
    # Initialize chat sessions
    if "chat_sessions" not in st.session_state:
        logger.debug("Initializing chat_sessions")
        st.session_state.chat_sessions = {"New Chat": []}
        st.session_state.current_chat = "New Chat"
    
    # Initialize chat titles
    if "chat_titles" not in st.session_state:
        logger.debug("Initializing chat_titles")
        st.session_state.chat_titles = {}
    
    # Message processing state
    if "messages" not in st.session_state:
        logger.debug("Initializing messages")
        st.session_state.messages = []
        
    if "thinking" not in st.session_state:
        logger.debug("Initializing thinking")
        st.session_state.thinking = False
        
    if "needs_response" not in st.session_state:
        logger.debug("Initializing needs_response")
        st.session_state.needs_response = False
    
    # API status tracking
    if "api_status_checked" not in st.session_state:
        logger.debug("Initializing api_status_checked")
        st.session_state.api_status_checked = False
        st.session_state.api_status = None
    
    # UI state for chat rename
    if "show_rename_input" not in st.session_state:
        logger.debug("Initializing show_rename_input")
        st.session_state.show_rename_input = False
    
    logger.debug("Session state initialization complete")

def get_current_chat_messages() -> List[Dict[str, str]]:
    """
    Get the messages for the current chat.
    
    Returns:
        List[Dict[str, str]]: List of message dictionaries
    """
    if "messages" not in st.session_state:
        return []
    return st.session_state.messages

def get_chat_title(chat_name: Optional[str] = None) -> str:
    """
    Get the title for a chat.
    
    Args:
        chat_name (str, optional): Name of the chat. If None, uses current chat.
        
    Returns:
        str: Chat title
    """
    if chat_name is None:
        chat_name = st.session_state.current_chat
    
    # If we have a stored title, use it
    if chat_name in st.session_state.chat_titles:
        return st.session_state.chat_titles[chat_name]
    
    # Default to chat name
    return chat_name

def create_new_chat() -> str:
    """
    Create a new chat and make it the current chat.
    
    Returns:
        str: Name of the new chat
    """
    logger.info("Creating new chat")
    
    # Create a new chat with a timestamp
    new_chat_name = f"Chat {time.strftime('%H:%M')}"
    st.session_state.chat_sessions[new_chat_name] = []
    st.session_state.current_chat = new_chat_name
    
    # Reset messages for the new chat
    st.session_state.messages = []
    
    logger.info(f"Created new chat: {new_chat_name}")
    return new_chat_name

def switch_to_chat(chat_name: str):
    """
    Switch to a different chat.
    
    Args:
        chat_name (str): Name of the chat to switch to
    """
    if chat_name not in st.session_state.chat_sessions:
        logger.warning(f"Attempted to switch to non-existent chat: {chat_name}")
        return
    
    logger.info(f"Switching to chat: {chat_name}")
    st.session_state.current_chat = chat_name
    
    # Update messages with the selected chat history
    st.session_state.messages = st.session_state.chat_sessions[chat_name]

def delete_chat(chat_name: str) -> Optional[str]:
    """
    Delete a chat and switch to another one if needed.
    
    Args:
        chat_name (str): Name of the chat to delete
        
    Returns:
        Optional[str]: Name of the new current chat, or None if operation failed
    """
    if chat_name not in st.session_state.chat_sessions:
        logger.warning(f"Attempted to delete non-existent chat: {chat_name}")
        return None
    
    if len(st.session_state.chat_sessions) <= 1:
        logger.warning("Attempted to delete the only chat")
        return None
    
    logger.info(f"Deleting chat: {chat_name}")
    
    # Delete the chat
    del st.session_state.chat_sessions[chat_name]
    
    # If we deleted the current chat, switch to another chat
    if chat_name == st.session_state.current_chat:
        new_current = list(st.session_state.chat_sessions.keys())[0]
        switch_to_chat(new_current)
        return new_current
    
    return st.session_state.current_chat

def rename_chat(chat_name: str, new_name: str) -> bool:
    """
    Rename a chat.
    
    Args:
        chat_name (str): Current name of the chat
        new_name (str): New name for the chat
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not new_name.strip():
        logger.warning("Attempted to rename chat with empty name")
        return False
    
    if chat_name not in st.session_state.chat_sessions:
        logger.warning(f"Attempted to rename non-existent chat: {chat_name}")
        return False
    
    logger.info(f"Renaming chat '{chat_name}' to '{new_name}'")
    
    # Rename chat
    messages = st.session_state.chat_sessions[chat_name]
    
    # Delete old chat
    del st.session_state.chat_sessions[chat_name]
    
    # Create new chat with renamed title
    st.session_state.chat_sessions[new_name] = messages
    
    # Update current chat if needed
    if chat_name == st.session_state.current_chat:
        st.session_state.current_chat = new_name
        st.session_state.messages = messages
    
    # Update chat title
    if chat_name in st.session_state.chat_titles:
        st.session_state.chat_titles[new_name] = st.session_state.chat_titles[chat_name]
        del st.session_state.chat_titles[chat_name]
    else:
        st.session_state.chat_titles[new_name] = new_name
    
    return True

def update_chat_title(chat_name: str, title: str):
    """
    Update the title of a chat.
    
    Args:
        chat_name (str): Name of the chat
        title (str): New title for the chat
    """
    logger.debug(f"Updating title for chat '{chat_name}' to '{title}'")
    st.session_state.chat_titles[chat_name] = title

def add_message(role: str, content: str):
    """
    Add a message to the current chat.
    
    Args:
        role (str): Role of the message sender ('user' or 'assistant')
        content (str): Content of the message
    """
    # Add message to chat history
    st.session_state.messages.append({"role": role, "content": content})
    
    # Update the chat session history
    chat_name = st.session_state.current_chat
    st.session_state.chat_sessions[chat_name] = st.session_state.messages
    
    logger.debug(f"Added {role} message to chat '{chat_name}'")

def get_all_chats() -> Dict[str, List[Dict[str, str]]]:
    """
    Get all available chats.
    
    Returns:
        Dict[str, List[Dict[str, str]]]: Dictionary of chat names to message lists
    """
    if "chat_sessions" not in st.session_state:
        return {}
    return st.session_state.chat_sessions

def get_chat_display_name(chat_name: str) -> str:
    """
    Get the display name for a chat (title if available).
    
    Args:
        chat_name (str): Internal name of the chat
        
    Returns:
        str: Display name for the chat
    """
    if chat_name in st.session_state.chat_titles:
        return st.session_state.chat_titles[chat_name]
    return chat_name 