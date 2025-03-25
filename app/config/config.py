"""
Configuration module for the Mistral AI Chat application.
Handles secure loading of API keys and application settings.
"""
import os
import logging
from typing import Dict, Any, List, Optional
import streamlit as st
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_config() -> Dict[str, Any]:
    """
    Load configuration from environment variables or .env file.
    Uses caching to avoid reloading on each Streamlit rerun.
    
    Returns:
        Configuration dictionary
    """
    # Try to load .env file if it exists
    load_dotenv()

    # Try to get API key from Streamlit secrets, then environment variables
    api_key = _get_api_key()
    
    if not api_key:
        logger.error("MISTRAL_API_KEY not found in environment variables or .env file")
        raise ValueError("MISTRAL_API_KEY not found. Please set the environment variable or add it to .env file.")
    
    # Create configuration dictionary
    config = {
        "api_key": api_key,
        "available_models": _get_available_models(),
        "default_model": _get_default_model(),
        "max_image_size_mb": _get_max_image_size(),
        "allowed_image_types": ["jpg", "jpeg", "png"],
    }
    
    logger.info("Configuration loaded successfully")
    return config

def _get_api_key() -> Optional[str]:
    """
    Get API key from various sources (secrets, environment variables).
    
    Returns:
        API key if found, None otherwise
    """
    # First try from Streamlit secrets
    try:
        api_key = st.secrets.get("MISTRAL_API_KEY")
        if api_key:
            logger.debug("Found API key in Streamlit secrets")
            return api_key
    except Exception:
        pass
    
    # Then try from environment variable
    api_key = os.environ.get("MISTRAL_API_KEY")
    if api_key:
        logger.debug("Found API key in environment variables")
        return api_key
    
    return None

def _get_available_models() -> List[str]:
    """
    Get list of available models.
    
    Returns:
        List of model identifiers
    """
    # Try to get from environment variable first
    models_str = os.environ.get("MISTRAL_AVAILABLE_MODELS")
    if models_str:
        try:
            models = [m.strip() for m in models_str.split(",")]
            logger.debug(f"Using models from environment: {models}")
            return models
        except Exception as e:
            logger.warning(f"Error parsing MISTRAL_AVAILABLE_MODELS: {e}")
    
    # Default models
    return [
        "mistral-small-latest",
        "mistral-medium-latest",
        "mistral-large-latest"
    ]

def _get_default_model() -> str:
    """
    Get default model to use.
    
    Returns:
        Default model identifier
    """
    default_model = os.environ.get("MISTRAL_DEFAULT_MODEL", "mistral-small-latest")
    logger.debug(f"Using default model: {default_model}")
    return default_model

def _get_max_image_size() -> int:
    """
    Get maximum image size in MB.
    
    Returns:
        Maximum image size in MB
    """
    try:
        size = int(os.environ.get("MAX_IMAGE_SIZE_MB", "5"))
        logger.debug(f"Using max image size: {size}MB")
        return size
    except ValueError:
        logger.warning("Invalid MAX_IMAGE_SIZE_MB value, using default of 5MB")
        return 5 