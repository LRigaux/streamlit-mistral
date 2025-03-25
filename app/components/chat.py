"""
Chat interface component for the Streamlit app.
Handles chat history, user input, and image uploads.
"""
import streamlit as st
from typing import Dict, List, Optional, Any
from PIL import Image
import logging
import re
from app.utils.mistral_client import get_mistral_client, chat_with_mistral
from app.config.config import load_config
from app.static.styles import get_fixed_input_css, get_scroll_to_input_js
from app.state.session_state import (
    get_current_chat_messages,
    get_chat_title,
    update_chat_title,
    add_message
)

logger = logging.getLogger(__name__)

class ChatInterface:
    """Chat interface component for the Streamlit application."""
    
    def __init__(self, default_model: str):
        """
        Initialize the chat interface.
        
        Args:
            default_model: Default Mistral model to use
        """
        self.default_model = default_model
        self.client = get_mistral_client()
        self.config = load_config()
    
    def render(self):
        """Render the chat interface with a fixed input area."""
        # Use a 2-row layout: chat history in top (scrollable), input in bottom (fixed)
        chat_history_container = st.container()
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)  # Spacer
        
        # Fixed bottom input container - will use custom CSS to keep at bottom
        input_container = st.container()
        
        # Process pending message if needed
        if st.session_state.needs_response:
            logger.info("Processing pending message...")
            self._process_pending_message()
            # Force a rerun to update the UI after processing
            st.rerun()
        
        # Get the current chat title or derive from first message
        current_title = get_chat_title()
            
        # Display the chat title
        with chat_history_container:
            if current_title:
                # Allow editing the title
                new_title = st.text_input("Chat title", value=current_title, key="chat_title_input")
                if new_title != current_title and new_title.strip():
                    # Update the chat title
                    update_chat_title(st.session_state.current_chat, new_title.strip())
                    # Force refresh
                    st.rerun()
            
            # Display chat history in the scrollable area
            self._display_chat_history()
        
        # Create the fixed input container
        with input_container:
            # Mark the input area with a special div we can target with CSS
            st.markdown("<div id='fixed-input-container'></div>", unsafe_allow_html=True)
            
            # Add custom CSS and JavaScript for fixed input and scrolling
            st.markdown(get_fixed_input_css(), unsafe_allow_html=True)
            st.markdown(f"<script>{get_scroll_to_input_js()}</script>", unsafe_allow_html=True)
            
            # Upload image option with cleaner layout
            col1, col2 = st.columns([1, 3])
            
            with col1:
                uploaded_file = st.file_uploader(
                    "Image", 
                    type=self.config["allowed_image_types"],
                    label_visibility="collapsed",
                    help="Upload an image to analyze with Mistral multimodal model"
                )
            
            # Check if an image was uploaded
            image = None
            if uploaded_file is not None:
                try:
                    image = Image.open(uploaded_file)
                    with col2:
                        st.image(image, use_column_width=True)
                except Exception as e:
                    st.error(f"Error opening image: {str(e)}")
            
            # User input with model selection - cleaner design
            with st.form(key="chat_form", clear_on_submit=True):
                # Message input area
                user_input = st.text_area(
                    "Message",
                    key="user_input",
                    height=120,
                    placeholder="Type your message here...",
                    label_visibility="collapsed"
                )
                
                # Model and token controls in a more subtle layout
                cols = st.columns([3, 2, 2, 1])
                
                with cols[0]:
                    st.caption("Customize your response:")
                
                with cols[1]:
                    selected_model = st.selectbox(
                        "Model",
                        options=self.config["available_models"],
                        index=self.config["available_models"].index(self.default_model),
                        label_visibility="collapsed"
                    )
                
                with cols[2]:
                    max_tokens = st.number_input(
                        "Tokens",
                        min_value=50,
                        max_value=4000,
                        value=500,
                        step=50,
                        help="Maximum number of tokens in the response",
                        label_visibility="collapsed"
                    )
                
                with cols[3]:
                    submit_button = st.form_submit_button("Send")
                
                # Handle form submission
                if submit_button and user_input:
                    self._handle_user_message(user_input, image, selected_model, max_tokens)
    
    def _handle_user_message(self, user_input: str, image: Optional[Image.Image], 
                             selected_model: str, max_tokens: int):
        """
        Handle a new user message submission.
        
        Args:
            user_input: The user's message
            image: Optional image uploaded by user
            selected_model: Selected Mistral model
            max_tokens: Maximum number of tokens for response
        """
        logger.info(f"User submitted message: {user_input[:20]}...")
        logger.info(f"Using model: {selected_model}, max tokens: {max_tokens}")
        
        # Store the message, image and parameters in session state
        st.session_state.last_user_input = user_input
        st.session_state.last_image = image
        st.session_state.selected_model = selected_model
        st.session_state.max_tokens = max_tokens
        
        # Add message to chat history
        add_message("user", user_input)
        
        # Update chat title based on first message if needed
        if len(st.session_state.messages) == 1:
            # Extract a title from the first message
            self._update_chat_title_from_message(user_input)
        
        # Set flags for processing
        st.session_state.thinking = True
        st.session_state.needs_response = True
        
        # Trigger rerun to show thinking indicator
        st.rerun()
    
    def _derive_title_from_message(self, message: str) -> str:
        """
        Derive a title from a message content.
        
        The title is derived by:
        1. Using the full message if it's shorter than 40 characters
        2. Finding a natural sentence break before 40 characters
        3. Truncating with ellipsis as a fallback
        
        Args:
            message: The message text to derive a title from
            
        Returns:
            A string containing the derived title
        """
        # Truncate to max ~40 chars, trying to break at sentence if possible
        max_length = 40
        if len(message) <= max_length:
            return message
        
        # Try to find a sentence break
        sentences = re.split(r'(?<=[.!?])\s+', message[:max_length+20])
        if sentences:
            # Return the first sentence, or truncate if it's too long
            first_sentence = sentences[0]
            if len(first_sentence) <= max_length + 10:
                return first_sentence
        
        # Fallback to truncating with ellipsis
        return message[:max_length] + "..."
    
    def _update_chat_title_from_message(self, message: str):
        """
        Update the chat title based on a message.
        
        Args:
            message: Message to derive title from
        """
        title = self._derive_title_from_message(message)
        update_chat_title(st.session_state.current_chat, title)
    
    def _display_chat_history(self):
        """Display the chat history with improved styling."""
        # Create a container for the chat history
        chat_container = st.container()
        
        with chat_container:
            # Empty space before starting messages for better spacing
            messages = get_current_chat_messages()
            if not messages:
                st.markdown("""
                <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 400px; opacity: 0.6;">
                    <div style="font-size: 1.5em; margin-bottom: 1em;">Begin a new conversation</div>
                    <div>Type a message below to start chatting with Mistral AI</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Display messages
            for idx, message in enumerate(messages):
                with st.chat_message(message["role"]):
                    st.write(message["content"])
            
            # Show thinking indicator with subtle animation
            if st.session_state.thinking:
                with st.chat_message("assistant"):
                    # Animated thinking indicator
                    st.markdown("""
                    <div style="display: flex; align-items: center;">
                      <div style="margin-right: 10px;">Thinking</div>
                      <div class="typing-dots">
                        <span style="animation-delay: 0s;"></span>
                        <span style="animation-delay: 0.2s;"></span>
                        <span style="animation-delay: 0.4s;"></span>
                      </div>
                    </div>
                    
                    <style>
                    .typing-dots {
                      display: flex;
                    }
                    .typing-dots span {
                      display: inline-block;
                      width: 6px;
                      height: 6px;
                      border-radius: 50%;
                      background-color: #888;
                      margin: 0 2px;
                      animation: pulse 1.5s infinite ease-in-out;
                    }
                    @keyframes pulse {
                      0%, 100% { transform: scale(1); opacity: 0.6; }
                      50% { transform: scale(1.5); opacity: 1; }
                    }
                    </style>
                    """, unsafe_allow_html=True)
    
    def _process_pending_message(self):
        """Process the last user message that needs a response."""
        if not st.session_state.needs_response:
            logger.warning("_process_pending_message called but no message needs response")
            return
            
        logger.info("Processing message...")
        
        try:
            with st.spinner("Getting response from Mistral AI..."):
                if "last_user_input" not in st.session_state:
                    logger.error("No last_user_input found in session state")
                    st.session_state.thinking = False
                    st.session_state.needs_response = False
                    return
                    
                user_input = st.session_state.last_user_input
                image = st.session_state.last_image if "last_image" in st.session_state else None
                selected_model = st.session_state.selected_model if "selected_model" in st.session_state else self.default_model
                max_tokens = st.session_state.max_tokens if "max_tokens" in st.session_state else 500
                
                logger.info(f"Processing message: {user_input[:20]}...")
                
                # Prepare messages for API call - exclude the "thinking..." message if it exists
                messages = []
                for m in st.session_state.messages:
                    # Skip any assistant "thinking..." messages
                    if m["role"] == "assistant" and m["content"] == "Thinking...":
                        continue
                    messages.append({"role": m["role"], "content": m["content"]})
                
                # Get response from Mistral API
                logger.info(f"Calling Mistral API with {len(messages)} messages, model: {selected_model}, max_tokens: {max_tokens}")
                response = chat_with_mistral(
                    client=self.client,
                    model=selected_model,
                    messages=messages,
                    image=image,
                    max_tokens=max_tokens
                )
                
                logger.info(f"Got response from API: {response[:20]}...")
                
                # Add assistant response to chat history
                add_message("assistant", response)
        
        except Exception as e:
            # Add error message to chat
            error_msg = f"Error: {str(e)}"
            logger.error(f"Error processing message: {str(e)}")
            add_message("assistant", error_msg)
            
        finally:
            # Clear thinking state and needs_response flag
            logger.info("Clearing thinking state and needs_response flag")
            st.session_state.thinking = False
            st.session_state.needs_response = False
            
            # Clear saved input and image
            if "last_user_input" in st.session_state:
                del st.session_state.last_user_input
            if "last_image" in st.session_state:
                del st.session_state.last_image 