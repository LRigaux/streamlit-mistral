"""
Sidebar component for the Streamlit app.
Displays model selection, API status, and settings.
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
        tuple: (selected_model, api_status)
    """
    with st.sidebar:
        st.title("Settings")
        
        # Load configuration
        config = load_config()
        
        # Check API connection status on load
        if "api_status_checked" not in st.session_state:
            st.session_state.api_status_checked = False
            st.session_state.api_status = None
        
        # Model selection
        st.header("Model")
        selected_model = st.selectbox(
            "Select Mistral Model",
            options=config["available_models"],
            index=config["available_models"].index(config["default_model"]),
            help="Choose which Mistral AI model to use for chat"
        )
        
        # API connection status
        st.header("API Status")
        
        # Test connection automatically on first load
        if not st.session_state.api_status_checked:
            with st.spinner("Testing API connection..."):
                try:
                    logger.info("Testing API connection on startup")
                    api_status = test_api_connection()
                    st.session_state.api_status = api_status
                    st.session_state.api_status_checked = True
                    
                    if api_status:
                        st.success("✅ Connected to Mistral API")
                        logger.info("API connection test successful")
                    else:
                        st.error("❌ Failed to connect to Mistral API")
                        logger.error("API connection test failed")
                except Exception as e:
                    st.error(f"❌ Error testing API: {str(e)}")
                    logger.exception("Error during API connection test")
                    st.session_state.api_status = False
                    st.session_state.api_status_checked = True
        else:
            # Display current status
            if st.session_state.api_status:
                st.success("✅ Connected to Mistral API")
            else:
                st.error("❌ Failed to connect to Mistral API")
        
        # Manual test button
        if st.button("Test API Connection Again"):
            with st.spinner("Testing connection..."):
                try:
                    logger.info("Manually testing API connection")
                    api_status = test_api_connection()
                    st.session_state.api_status = api_status
                    
                    if api_status:
                        st.success("✅ Connected to Mistral API")
                        logger.info("Manual API connection test successful")
                    else:
                        st.error("❌ Failed to connect to Mistral API")
                        logger.error("Manual API connection test failed")
                except Exception as e:
                    st.error(f"❌ Error testing API: {str(e)}")
                    logger.exception("Error during manual API connection test")
                    st.session_state.api_status = False
        
        # Information about the application
        st.header("About")
        st.markdown("""
        This application uses Mistral AI's models to provide chat and image analysis capabilities.
        """)
        
        
        # Footer
        st.markdown("---")
        st.caption("LRIGAUX -Mistral AI Chat App © 2025")
    
    return selected_model, st.session_state.api_status 