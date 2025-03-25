"""
Streamlit application for Mistral AI chat interface.
This app provides a simple interface for chatting with Mistral AI's models and uploading images.
"""
import os
import logging
import streamlit as st
from app.config.config import load_config
from app.utils.logging_util import setup_logging
from app.components.chat import ChatInterface
from app.components.sidebar import create_sidebar
from app.state.session_state import initialize_session_state
from app.static.styles import get_app_css, get_keyboard_shortcuts_js

# Import logo module (create directory structure if needed)
try:
    from app.static.logo import display_logo, display_brand, FAVICON, display_header
except ImportError:
    # Define fallback logo if import fails
    def display_brand():
        return "<h1>LRIGSCHAT</h1>"
    def display_header():
        return "<div style='height: 3rem;'></div>"
    def display_logo():
        return ""
    FAVICON = ""

# Set up logging (with file logging in production)
if os.environ.get("STREAMLIT_ENV") == "production":
    logger = setup_logging(log_level=logging.INFO, log_to_file=True)
else:
    logger = setup_logging(log_level=logging.DEBUG)

# Set page configuration
st.set_page_config(
    page_title="LRIGSCHAT",
    page_icon="🔮",
    layout="wide",
)

def main():
    """Main function to run the Streamlit application."""
    logger.info("Starting LRIGSCHAT application")
    
    try:
        # Initialize session state
        logger.info("Initializing session state")
        initialize_session_state()
        
        # Load configuration
        logger.info("Loading configuration")
        config = load_config()
        logger.debug(f"Configuration loaded: {list(config.keys())}")
        
        # Apply custom CSS and JavaScript
        st.markdown(get_app_css(), unsafe_allow_html=True)
        st.markdown(f"<script>{get_keyboard_shortcuts_js()}</script>", unsafe_allow_html=True)
        
        # Display the fixed header
        st.markdown(display_header(), unsafe_allow_html=True)
        
        # Create sidebar
        logger.info("Creating sidebar")
        default_model, api_status = create_sidebar()
        
        # Display logo and brand at the top of the main content
        st.markdown(display_brand(), unsafe_allow_html=True)
        
        # Hidden title (for accessibility)
        st.title("LRIGSCHAT")
        
        # Check API status before initializing chat interface
        if api_status is False:
            st.error("❌ Unable to connect to Mistral API. Please check your API key and try again.")
            st.info("Make sure the MISTRAL_API_KEY environment variable is correctly set.")
            return
        
        # Initialize chat interface
        logger.info(f"Initializing chat interface with default model: {default_model}")
        chat_interface = ChatInterface(default_model)
        chat_interface.render()
        
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        st.error(f"Configuration error: {str(e)}")
        
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        st.error(f"An unexpected error occurred: {str(e)}")
        st.info("Check the logs for more information.")

if __name__ == "__main__":
    main() 