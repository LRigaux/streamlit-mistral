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

# Set up logging (with file logging in production)
if os.environ.get("STREAMLIT_ENV") == "production":
    logger = setup_logging(log_level=logging.INFO, log_to_file=True)
else:
    logger = setup_logging(log_level=logging.DEBUG)

# Set page configuration
st.set_page_config(
    page_title="Mistral AI Chat",
    page_icon="🔮",
    layout="wide",
)

def main():
    """Main function to run the Streamlit application."""
    logger.info("Starting Mistral AI Chat application")
    
    try:
        # Load configuration
        logger.info("Loading configuration")
        config = load_config()
        logger.debug(f"Configuration loaded: {list(config.keys())}")
        
        # Custom CSS with color palette from the image (autumn colors)
        st.markdown("""
        <style>
        /* Color palette */
        :root {
            --dark-purple: #3A2A3A;
            --burgundy: #87404D;
            --red: #A82C3A;
            --orange: #DE7921;
            --yellow: #F9C80E;
        }
        
        /* Apply colors to elements */
        .stApp {
            background-color: var(--dark-purple);
            color: white;
        }
        
        .stButton>button {
            background-color: var(--burgundy);
            color: white;
            border: none;
        }
        
        .stButton>button:hover {
            background-color: var(--red);
        }
        
        h1, h2, h3 {
            color: var(--yellow);
        }
        
        .stTextInput>div>div>input {
            border-color: var(--orange);
        }
        
        .stSidebar {
            background-color: rgba(58, 42, 58, 0.9);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create sidebar
        logger.info("Creating sidebar")
        selected_model, api_status = create_sidebar()
        
        # Main content area
        st.title("Mistral AI Chat Assistant 🔮")
        
        # Check API status before initializing chat interface
        if api_status is False:
            st.error("❌ Impossible de se connecter à l'API Mistral. Veuillez vérifier votre clé API et réessayer.")
            st.info("Vérifiez que la variable d'environnement MISTRAL_API_KEY est correctement définie.")
            return
        
        # Initialize chat interface
        logger.info(f"Initializing chat interface with model: {selected_model}")
        chat_interface = ChatInterface(selected_model)
        chat_interface.render()
        
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        st.error(f"Erreur de configuration: {str(e)}")
        
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        st.error(f"Une erreur inattendue s'est produite: {str(e)}")
        st.info("Consultez les logs pour plus d'informations.")

if __name__ == "__main__":
    main() 