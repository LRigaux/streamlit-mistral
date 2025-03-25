"""
Mistral client utility module.
Provides functions to interact with the Mistral AI API.
"""
import os
import logging
import base64
import time
from typing import List, Dict, Optional, Any, Union
from mistralai import Mistral
from PIL import Image
from io import BytesIO
import streamlit as st

logger = logging.getLogger(__name__)

class RateLimiter:
    """Simple rate limiter for API calls."""
    
    def __init__(self, calls_per_minute: int = 60):
        """
        Initialize a rate limiter.
        
        Args:
            calls_per_minute: Maximum number of calls allowed per minute
        """
        self.calls_per_minute = calls_per_minute
        self.call_times = []
        logger.debug(f"Initialized rate limiter with {calls_per_minute} calls per minute")
    
    def wait_if_needed(self):
        """
        Wait if we've exceeded our rate limit.
        This method will block until it's safe to make another API call.
        """
        now = time.time()
        # Remove calls older than 1 minute
        self.call_times = [t for t in self.call_times if now - t < 60]
        
        if len(self.call_times) >= self.calls_per_minute:
            # Wait until we can make another call
            oldest_call = self.call_times[0]
            wait_time = 60 - (now - oldest_call)
            if wait_time > 0:
                logger.debug(f"Rate limit reached, waiting {wait_time:.2f} seconds")
                time.sleep(wait_time)
        
        # Add this call to the list
        self.call_times.append(time.time())

# Create a global rate limiter instance
rate_limiter = RateLimiter()

@st.cache_resource
def get_mistral_client(api_key: Optional[str] = None) -> Mistral:
    """
    Initialize and return a Mistral AI client.
    Uses Streamlit caching to avoid recreating the client on each rerun.
    
    Args:
        api_key: Mistral API key. If None, get from environment.
        
    Returns:
        Initialized Mistral client
        
    Raises:
        ValueError: If API key is not provided or found in environment
    """
    if not api_key:
        # Try to get from Streamlit secrets
        try:
            api_key = st.secrets.get("MISTRAL_API_KEY")
        except:
            pass
            
        # If not in Streamlit secrets, try environment variables
        if not api_key:
            api_key = os.environ.get("MISTRAL_API_KEY")
        
    if not api_key:
        logger.error("MISTRAL_API_KEY not found")
        raise ValueError("MISTRAL_API_KEY not found")
    
    try:
        client = Mistral(api_key=api_key)
        logger.info("Mistral client initialized successfully")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Mistral client: {str(e)}")
        raise

@st.cache_data(ttl=300)  # Cache for 5 minutes
def test_api_connection(api_key: Optional[str] = None) -> bool:
    """
    Test the connection to Mistral API.
    Uses caching to reduce API calls for repeated tests.
    
    Args:
        api_key: Mistral API key. If None, get from environment.
        
    Returns:
        True if connection is successful, False otherwise
    """
    try:
        client = get_mistral_client(api_key)
        # Simple test query
        logger.info("Testing API connection with a simple query...")
        rate_limiter.wait_if_needed()
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": "Hello, are you connected?"}],
            max_tokens=10
        )
        logger.info(f"API connection test successful, received response: {response.choices[0].message.content}")
        return True
    except Exception as e:
        logger.error(f"API connection test failed with unexpected error: {str(e)}")
        return False

def encode_image_to_base64(image_path: str) -> str:
    """
    Encode an image to base64 for use with Mistral multimodal models.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Base64 encoded image
    """
    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            base64_encoded = base64.b64encode(image_data).decode("utf-8")
            return base64_encoded
    except Exception as e:
        logger.error(f"Failed to encode image: {str(e)}")
        raise

def encode_pil_image_to_base64(pil_image: Image.Image) -> str:
    """
    Encode a PIL Image to base64 for use with Mistral multimodal models.
    
    Args:
        pil_image: PIL Image object
        
    Returns:
        Base64 encoded image
    """
    try:
        buffer = BytesIO()
        pil_image.save(buffer, format="PNG")
        base64_encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return base64_encoded
    except Exception as e:
        logger.error(f"Failed to encode PIL image: {str(e)}")
        raise

def chat_with_mistral(
    client: Mistral, 
    model: str, 
    messages: List[Dict[str, str]], 
    image: Optional[Image.Image] = None, 
    max_tokens: int = 500, 
    max_retries: int = 3, 
    timeout: int = 60
) -> str:
    """
    Send a chat request to Mistral API, with optional image.
    
    Args:
        client: Initialized Mistral client
        model: Model name to use
        messages: List of message dictionaries
        image: PIL Image to include with request
        max_tokens: Maximum number of tokens in the response
        max_retries: Maximum number of retries on failure
        timeout: Timeout in seconds for the API call
        
    Returns:
        Response from the model
    """
    start_time = time.time()
    retries = 0
    
    # Log the request
    logger.info(f"Sending chat request to Mistral API using model: {model}")
    logger.info(f"Number of messages: {len(messages)}")
    logger.info(f"Max tokens: {max_tokens}")
    if image:
        logger.info("Request includes an image")
    
    while retries <= max_retries:
        try:
            # Apply rate limiting
            rate_limiter.wait_if_needed()
            
            # Handle image if provided (for multimodal)
            processed_messages = messages.copy()
            if image:
                # Encode image to base64
                logger.info("Encoding image to base64")
                base64_image = encode_pil_image_to_base64(image)
                
                # Modify the last message to include the image
                last_msg = processed_messages[-1]
                logger.info(f"Adding image to message with text: {last_msg['content']}")
                content = [
                    {"type": "text", "text": last_msg["content"]},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ]
                processed_messages[-1]["content"] = content
            
            # Check for timeout
            if time.time() - start_time > timeout:
                logger.error(f"Request timed out after {timeout} seconds")
                return f"Error: Request timed out after {timeout} seconds. Please try again."
            
            # Send request to Mistral API
            logger.info("Sending request to Mistral API...")
            response = client.chat.complete(
                model=model,
                messages=processed_messages,
                max_tokens=max_tokens
            )
            
            response_content = response.choices[0].message.content
            logger.info(f"Received response from Mistral API (length: {len(response_content)} chars)")
            return response_content
                
        except ConnectionError as e:
            logger.warning(f"Connection error (attempt {retries+1}/{max_retries}): {str(e)}")
            retries += 1
            if retries <= max_retries:
                # Exponential backoff
                sleep_time = 2 ** retries
                logger.info(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                return f"Connection error: {str(e)}. Please check your internet connection and try again."
        
        except TimeoutError as e:
            logger.warning(f"Timeout error (attempt {retries+1}/{max_retries}): {str(e)}")
            retries += 1
            if retries <= max_retries:
                sleep_time = 2 ** retries
                logger.info(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                return f"Operation timed out. The server might be experiencing high load. Please try again later."
                
        except Exception as e:
            logger.error(f"Unexpected error when calling Mistral API: {str(e)}")
            return f"Error: {str(e)}"
    
    # This should only happen if all retries are exhausted
    return "Error: Could not get a response after multiple attempts. Please try again later."

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_available_models() -> List[str]:
    """
    Fetch available models from the Mistral API.
    Cached to reduce API calls.
    
    Returns:
        List of available model names
    """
    # Hardcoded models as a fallback
    default_models = [
        "mistral-small-latest",
        "mistral-medium-latest",
        "mistral-large-latest"
    ]
    
    try:
        client = get_mistral_client()
        rate_limiter.wait_if_needed()
        # This is a placeholder - the actual API might have a different method
        # to list available models
        models = client.list_models()
        return [model.id for model in models]
    except Exception as e:
        logger.warning(f"Failed to fetch available models: {str(e)}")
        logger.info("Using default model list as fallback")
        return default_models 