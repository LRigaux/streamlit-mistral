"""
Mistral client utility module.
Provides functions to interact with the Mistral AI API.
"""
import os
import logging
import base64
import time
from mistralai import Mistral
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)

def get_mistral_client(api_key=None):
    """
    Initialize and return a Mistral AI client.
    
    Args:
        api_key (str, optional): Mistral API key. If None, get from environment.
        
    Returns:
        Mistral: Initialized Mistral client
        
    Raises:
        ValueError: If API key is not provided or found in environment
    """
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

def test_api_connection(api_key=None):
    """
    Test the connection to Mistral API.
    
    Args:
        api_key (str, optional): Mistral API key. If None, get from environment.
        
    Returns:
        bool: True if connection is successful, False otherwise
    """
    try:
        client = get_mistral_client(api_key)
        # Simple test query
        logger.info("Testing API connection with a simple query...")
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

def encode_image_to_base64(image_path):
    """
    Encode an image to base64 for use with Mistral multimodal models.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Base64 encoded image
    """
    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            base64_encoded = base64.b64encode(image_data).decode("utf-8")
            return base64_encoded
    except Exception as e:
        logger.error(f"Failed to encode image: {str(e)}")
        raise

def encode_pil_image_to_base64(pil_image):
    """
    Encode a PIL Image to base64 for use with Mistral multimodal models.
    
    Args:
        pil_image (PIL.Image): PIL Image object
        
    Returns:
        str: Base64 encoded image
    """
    try:
        buffer = BytesIO()
        pil_image.save(buffer, format="PNG")
        base64_encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return base64_encoded
    except Exception as e:
        logger.error(f"Failed to encode PIL image: {str(e)}")
        raise

def chat_with_mistral(client, model, messages, image=None, max_retries=2, timeout=60):
    """
    Send a chat request to Mistral API, with optional image.
    
    Args:
        client (Mistral): Initialized Mistral client
        model (str): Model name to use
        messages (list): List of message dictionaries
        image (PIL.Image, optional): PIL Image to include with request
        max_retries (int): Maximum number of retries on failure
        timeout (int): Timeout in seconds for the API call
        
    Returns:
        str: Response from the model
    """
    start_time = time.time()
    retries = 0
    
    # Log the request
    logger.info(f"Sending chat request to Mistral API using model: {model}")
    logger.info(f"Number of messages: {len(messages)}")
    if image:
        logger.info("Request includes an image")
    
    while retries <= max_retries:
        try:
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
                return f"Erreur: La requête a expiré après {timeout} secondes. Veuillez réessayer."
            
            # Send request to Mistral API
            logger.info("Sending request to Mistral API...")
            response = client.chat.complete(
                model=model,
                messages=processed_messages
            )
            
            response_content = response.choices[0].message.content
            logger.info(f"Received response from Mistral API (length: {len(response_content)} chars)")
            return response_content
                
        except Exception as e:
            logger.error(f"Unexpected error when calling Mistral API: {str(e)}")
            return f"Erreur inattendue: {str(e)}"
    
    # This should only happen if all retries are exhausted
    return "Erreur: Impossible d'obtenir une réponse après plusieurs tentatives." 