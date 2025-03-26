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

# Import logo module (create directory structure if needed)
import importlib.util
try:
    os.makedirs("app/static", exist_ok=True)
    from app.static.logo import display_logo, display_brand, FAVICON, display_header
except:
    # Define fallback logo if import fails
    def display_brand():
        return "<h1>MISTRAL CHAT</h1>"
    def display_header():
        return "<div style='height: 3rem;'></div>"
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
    initial_sidebar_state="collapsed",
    
)

def main():
    """Main function to run the Streamlit application."""
    logger.info("Starting Mistral AI Chat application")
    
    try:
        # Load configuration
        logger.info("Loading configuration")
        config = load_config()
        logger.debug(f"Configuration loaded: {list(config.keys())}")
        
        # Custom CSS with minimal design inspired by Identités Studio
        st.markdown("""
        <style>
        /* Font and Base Styles */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            font-weight: 300;
        }
        
        /* Color palette - minimal with accent colors */
        :root {
            --bg-color: #FFFFFF;
            --text-color: #111111;
            --accent1: #A82C3A;  /* Red from autumn palette */
            --accent2: #DE7921;  /* Orange from autumn palette */
            --accent3: #3A2A3A;  /* Dark Purple from autumn palette */
            --light-gray: #F5F5F5;
            --medium-gray: #E0E0E0;
            --dark-gray: #666666;
        }
        
        /* Apply colors to elements */
        .stApp {
            background-color: var(--bg-color);
            color: var(--text-color);
        }
        
        /* Header styling */
        h1, h2, h3 {
            font-weight: 400;
            letter-spacing: -0.5px;
            color: var(--text-color);
        }
        
        h1 {
            font-size: 2.2rem;
            margin-bottom: 2rem;
        }
        
        h2 {
            font-size: 1.5rem;
            margin-top: 2rem;
        }
        
        /* Form styling */
        div[data-testid="stForm"] {
            background-color: var(--light-gray);
            padding: 1.5rem;
            border-radius: 0px;
            border: none;
            margin-top: 1rem;
            margin-bottom: 2rem;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: var(--accent1);
            color: white;
            border: none;
            border-radius: 0px;
            padding: 0.5rem 1.5rem;
            font-weight: 400;
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            background-color: var(--text-color);
            color: white;
            transform: translateY(-2px);
        }
        
        /* Input fields */
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            border-color: var(--medium-gray);
            border-radius: 0px;
        }
        
        .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
            border-color: var(--accent1);
            box-shadow: none;
        }
        
        /* Sidebar styling */
        .stSidebar {
            background-color: var(--bg-color);
            border-right: 1px solid var(--medium-gray);
        }
        
        /* File uploader */
        .stFileUploader > div > button {
            background-color: transparent;
            border: 1px dashed var(--medium-gray);
            border-radius: 0px;
            color: var(--dark-gray);
        }
        
        .stFileUploader > div > button:hover {
            border-color: var(--accent1);
            color: var(--accent1);
        }
        
        /* Chat messages */
        .stChatMessage {
            background-color: var(--light-gray);
            border-radius: 0px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .stChatMessage.user {
            background-color: var(--light-gray);
        }
        
        .stChatMessage.assistant {
            background-color: white;
            border-left: 3px solid var(--accent1);
        }
        
        /* Select boxes */
        .stSelectbox label, .stNumberInput label {
            color: var(--text-color) !important;
            font-weight: 400;
        }
        
        .stSelectbox > div > div, .stNumberInput > div > div {
            border-radius: 0px;
        }
        
        /* For all labels */
        label {
            font-weight: 400 !important;
            color: var(--text-color) !important;
        }
        
        /* Progress bar */
        .stProgress > div > div > div {
            background-color: var(--accent1);
        }
        
        /* Horizontal rule */
        hr {
            border-color: var(--medium-gray);
        }
        
        /* Footer text */
        .stFooter {
            color: var(--dark-gray);
            font-size: 0.8rem;
        }
        
        /* Make the chat area stand out more */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Customize scrollbar */
        ::-webkit-scrollbar {
            width: 5px;
            height: 5px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--light-gray);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--dark-gray);
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent1);
        }
        
        /* Hide main title - we'll use our custom logo instead */
        .main > div:first-child {
            height: 0;
            padding: 0;
            margin: 0;
        }

        /* Adjust sidebar scrolling to make room for fixed header */
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            padding-top: 3rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Display the fixed header
        st.header("LRIGSCHAT", divider="red")
        
        # Create sidebar
        logger.info("Creating sidebar")
        default_model, api_status = create_sidebar()
        
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