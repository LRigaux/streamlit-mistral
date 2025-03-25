"""
Chat interface component for the Streamlit app.
Handles chat history, user input, and image uploads.
"""
import streamlit as st
from PIL import Image
import logging
from app.utils.mistral_client import get_mistral_client, chat_with_mistral
from app.config.config import load_config

logger = logging.getLogger(__name__)

class ChatInterface:
    """Chat interface component for the Streamlit application."""
    
    def __init__(self, default_model):
        """
        Initialize the chat interface.
        
        Args:
            default_model (str): Default Mistral model to use
        """
        self.default_model = default_model
        self.client = get_mistral_client()
        self.config = load_config()
        
        # Initialize session state for chat history if not exists
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        if "thinking" not in st.session_state:
            st.session_state.thinking = False
            
        # Check if we need to process the last message
        if "needs_response" not in st.session_state:
            st.session_state.needs_response = False
            
        # Initialize chat sessions if needed
        if "chat_sessions" not in st.session_state:
            st.session_state.chat_sessions = {"New Chat": []}
            st.session_state.current_chat = "New Chat"
    
    def render(self):
        """Render the chat interface."""
        # Display chat messages
        self._display_chat_history()
        
        # Process pending message if needed
        if st.session_state.needs_response:
            logger.info("Processing pending message...")
            self._process_pending_message()
            # Force a rerun to update the UI after processing
            st.rerun()
        
        # Upload image option
        uploaded_file = st.file_uploader(
            "Upload an image (optional)", 
            type=["jpg", "jpeg", "png"],
            help="Upload an image to analyze with Mistral multimodal model"
        )
        
        # Check if an image was uploaded
        image = None
        if uploaded_file is not None:
            try:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_column_width=True)
            except Exception as e:
                st.error(f"Error opening image: {str(e)}")
        
        # User input with model selection
        with st.form(key="chat_form", clear_on_submit=True):
            cols = st.columns([3, 1, 1])
            
            with cols[0]:
                user_input = st.text_area("Your message:", key="user_input", height=100)
            
            with cols[1]:
                selected_model = st.selectbox(
                    "Model:",
                    options=self.config["available_models"],
                    index=self.config["available_models"].index(self.default_model)
                )
            
            with cols[2]:
                max_tokens = st.number_input(
                    "Max tokens:",
                    min_value=50,
                    max_value=4000,
                    value=500,
                    step=50,
                    help="Maximum number of tokens in the response"
                )
            
            submit_button = st.form_submit_button("Send")
            
            if submit_button and user_input:
                logger.info(f"User submitted message: {user_input[:20]}...")
                logger.info(f"Using model: {selected_model}, max tokens: {max_tokens}")
                
                # Store the message, image and parameters in session state
                st.session_state.last_user_input = user_input
                st.session_state.last_image = image
                st.session_state.selected_model = selected_model
                st.session_state.max_tokens = max_tokens
                
                # Add message to chat history
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Update the chat session history
                st.session_state.chat_sessions[st.session_state.current_chat] = st.session_state.messages
                
                # Set flags for processing
                st.session_state.thinking = True
                st.session_state.needs_response = True
                
                # Trigger rerun to show thinking indicator
                st.rerun()
    
    def _display_chat_history(self):
        """Display the chat history."""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Show thinking indicator
        if st.session_state.thinking:
            with st.chat_message("assistant"):
                st.write("Thinking...")
    
    def _process_pending_message(self):
        """Process the last user message that needs a response."""
        if not st.session_state.needs_response:
            logger.warning("_process_pending_message called but no message needs response")
            return
            
        logger.info("Processing message...")
        
        try:
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
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Update the session history
            st.session_state.chat_sessions[st.session_state.current_chat] = st.session_state.messages
            
        except Exception as e:
            # Add error message to chat
            error_msg = f"Error: {str(e)}"
            logger.error(f"Error processing message: {str(e)}")
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            
            # Update the session history
            st.session_state.chat_sessions[st.session_state.current_chat] = st.session_state.messages
        
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