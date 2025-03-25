"""
Unified tests for the Mistral AI Chat application.

This file groups API and chat tests in one place,
allowing you to quickly verify that everything works correctly.

Usage:
    python test.py api    # To test only the API connection
    python test.py chat   # To test a conversation with the model
    python test.py        # To run all tests
"""
import os
import sys
import logging
from dotenv import load_dotenv
from mistralai import Mistral
from app.utils.mistral_client import get_mistral_client, test_api_connection

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_api():
    """Test connection to the Mistral API."""
    logger.info("=== Testing Mistral API connection ===")
    
    # Load environment variables
    load_dotenv()
    # Get API key
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        logger.error("MISTRAL_API_KEY not found in environment variables")
        return False
    
    logger.info(f"API key found (first 4 characters: {api_key[:4]}...)")
    
    # Test client initialization
    try:
        logger.info("Initializing Mistral client...")
        client = get_mistral_client()
        logger.info("✓ Client initialized successfully")
    except Exception as e:
        logger.error(f"✗ Client initialization failed: {str(e)}")
        return False
    
    # Test API connection
    try:
        logger.info("Testing API connection...")
        connection_status = test_api_connection()
        
        if connection_status:
            logger.info("✓ API connection successful")
            return True
        else:
            logger.error("✗ API connection failed")
            return False
    except Exception as e:
        logger.error(f"✗ Error during connection test: {str(e)}")
        return False

def test_chat():
    """Test conversation with the Mistral model."""
    logger.info("=== Testing conversation with Mistral model ===")
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        logger.error("MISTRAL_API_KEY not found in environment variables")
        return False
    
    try:
        # Initialize client
        logger.info("Initializing Mistral client...")
        client = Mistral(api_key=api_key)
        
        # Test a simple conversation
        logger.info("Testing a simple conversation...")
        
        # Conversation
        conversation = []
        
        # First message
        user_message = "Hello! I'd like to know more about seasons. What's your favorite season and why?"
        logger.info(f"User: {user_message}")
        
        conversation.append({"role": "user", "content": user_message})
        
        # Get response
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=conversation,
            max_tokens=10

        )
        
        assistant_message = response.choices[0].message.content
        logger.info(f"Assistant: {assistant_message}")
        
        # Add to conversation
        conversation.append({"role": "assistant", "content": assistant_message})
        
        # Second message to test context
        user_message = "Can you tell me about the typical colors of autumn?"
        logger.info(f"User: {user_message}")
        
        conversation.append({"role": "user", "content": user_message})
        
        # Get response
        response = client.chat.complete(
            model="mistral-small-latest",
            messages=conversation,
            max_tokens=10
        )
        
        assistant_message = response.choices[0].message.content
        logger.info(f"Assistant: {assistant_message}")
        
        logger.info("✓ Conversation test successful")
        return True
    except Exception as e:
        logger.error(f"✗ Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Starting tests...")
    
    # Determine which tests to run based on arguments
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "api":
            # Run only API test
            success = test_api()
        elif sys.argv[1].lower() == "chat":
            # Run only chat test
            success = test_chat()
        else:
            logger.error(f"Invalid argument: {sys.argv[1]}")
            logger.info("Valid options: 'api', 'chat'")
            sys.exit(1)
    else:
        # Run all tests
        api_success = test_api()
        
        if api_success:
            chat_success = test_chat()
            success = api_success and chat_success
        else:
            logger.error("API test failed, chat test canceled")
            success = False
    
    # Display final result
    if success:
        logger.info("✅ All tests passed!")
        sys.exit(0)
    else:
        logger.error("❌ Some tests failed")
        sys.exit(1) 