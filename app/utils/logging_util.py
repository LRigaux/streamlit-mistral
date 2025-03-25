"""
Logging utility module for the Mistral AI Chat application.
"""
import os
import logging
import sys
from datetime import datetime

def setup_logging(log_level=logging.INFO, log_to_file=False):
    """
    Set up logging configuration for the application.
    
    Args:
        log_level (int): Logging level (e.g., logging.INFO, logging.DEBUG)
        log_to_file (bool): Whether to log to a file in addition to console
        
    Returns:
        logging.Logger: Configured logger
    """
    # Create logs directory if it doesn't exist
    if log_to_file and not os.path.exists("logs"):
        os.makedirs("logs")
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear any existing handlers
    if root_logger.handlers:
        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Add console handler to logger
    root_logger.addHandler(console_handler)
    
    # Add file handler if requested
    if log_to_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join("logs", f"mistral_chat_{timestamp}.log")
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        
        root_logger.addHandler(file_handler)
        root_logger.info(f"Logging to file: {log_file}")
    
    # Create application logger
    logger = logging.getLogger("mistral_chat")
    logger.info("Logging initialized")
    
    return logger 