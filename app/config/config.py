"""
Configuration module for the Mistral AI Chat application.
Handles secure loading of API keys and application settings.
"""
import os
import logging
import streamlit as st
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_config():
    """
    Load configuration from environment variables or .env file.
    
    Returns:
        dict: Configuration dictionary
    """

    api_key = st.secrets.get("MISTRAL_API_KEY")
    
    if not api_key:
        logger.error("MISTRAL_API_KEY not found in environment variables or .env file")
        raise ValueError("MISTRAL_API_KEY not found. Please set the environment variable or add it to .env file.")
    
    # Create configuration dictionary
    config = {
        "api_key": api_key,
        "available_models": [
            "mistral-small-latest",
            "mistral-medium-latest",
            "mistral-large-latest"
        ],
        "default_model": "mistral-small-latest",
        "max_image_size_mb": 5,
        "allowed_image_types": ["jpg", "jpeg", "png"],
    }
    
    logger.info("Configuration loaded successfully")
    return config 