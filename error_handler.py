import logging
import sys
import traceback
from typing import Callable, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("jarvis_assistant.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("jarvis_assistant")

class ErrorHandler:
    """Error handling utility class for the Jarvis AI Assistant"""
    
    @staticmethod
    def log_error(error: Exception, context: str = "") -> None:
        """Log an error with context information"""
        error_type = type(error).__name__
        error_message = str(error)
        
        if context:
            logger.error(f"{context} - {error_type}: {error_message}")
        else:
            logger.error(f"{error_type}: {error_message}")
        
        logger.debug(traceback.format_exc())
    
    @staticmethod
    def handle_api_error(error: Exception) -> str:
        """Handle API-related errors and return user-friendly messages"""
        error_message = str(error).lower()
        
        if "api key" in error_message or "authentication" in error_message:
            return "There seems to be an issue with the API key. Please check your .env file."
        elif "timeout" in error_message or "connection" in error_message:
            return "Unable to connect to the Gemini API. Please check your internet connection."
        elif "quota" in error_message or "limit" in error_message:
            return "You've reached your API usage limit. Please try again later."
        else:
            ErrorHandler.log_error(error, "API Error")
            return f"An error occurred while communicating with the AI service: {str(error)}"
    
    @staticmethod
    def safe_execute(func: Callable, *args, **kwargs) -> tuple[bool, Any, Optional[Exception]]:
        """Execute a function safely and return success status, result, and any exception"""
        try:
            result = func(*args, **kwargs)
            return True, result, None
        except Exception as e:
            ErrorHandler.log_error(e, f"Error in {func.__name__}")
            return False, None, e

# Example usage:
# try:
#     # Some code that might raise an exception
#     result = some_function()
# except Exception as e:
#     user_message = ErrorHandler.handle_api_error(e)
#     print(user_message)