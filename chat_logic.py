import os
import google.generativeai as genai
from dotenv import load_dotenv
from error_handler import ErrorHandler, logger
from typing import List, Dict, Any, Optional

# Load environment variables from .env file
load_dotenv()

class GeminiConfig:
    """Configuration class for Gemini API settings"""
    API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_NAME = 'gemini-2.5-flash'
    SAFETY_SETTINGS = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    ]

# Validate API key
if not GeminiConfig.API_KEY:
    logger.error("No API key found. Please set GEMINI_API_KEY in .env file")
    raise ValueError("Missing API key. Please set GEMINI_API_KEY in .env file")

# Configure the Gemini API client
genai.configure(api_key=GeminiConfig.API_KEY)

class ChatHistory:
    """Class to manage chat history and message handling"""
    def __init__(self, max_history_length: int = 20):
        self.messages: List[Dict[str, Any]] = []
        self.max_history_length = max_history_length
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the chat history"""
        if len(self.messages) >= self.max_history_length * 2:
            self.messages = self.messages[2:]
            logger.info(f"Trimmed chat history to {len(self.messages)} messages")
        
        self.messages.append({"role": role, "parts": [content]})
    
    def remove_last_user_message(self) -> None:
        """Remove the last user message from history"""
        if self.messages and self.messages[-1]["role"] == "user":
            self.messages.pop()
    
    def clear(self) -> None:
        """Clear all messages from history"""
        self.messages = []
        logger.info("Chat history cleared")

# Initialize chat history
chat_history = ChatHistory()

def chat_with_gemini(user_message: str) -> str:
    """
    Sends a user message to the Gemini model and returns the model's response.
    Maintains a chat history with a maximum length to prevent token limit issues.
    
    Args:
        user_message (str): The user's input message
        
    Returns:
        str: The AI model's response text
    """
    # Add user message to chat history
    chat_history.add_message("user", user_message)
    
    try:
        # Initialize the model with safety settings
        model = genai.GenerativeModel(
            GeminiConfig.MODEL_NAME,
            safety_settings=GeminiConfig.SAFETY_SETTINGS
        )
        
        # Generate content with the model
        response = model.generate_content(chat_history.messages)

        # Extract and validate response text
        model_response_text = extract_response_text(response)
        
        # Add the model's response to chat history
        chat_history.add_message("model", model_response_text)
        return model_response_text

    except Exception as e:
        error_message = ErrorHandler.handle_api_error(e)
        chat_history.remove_last_user_message()
        return error_message

def extract_response_text(response: Any) -> str:
    """Extract text from Gemini API response"""
    try:
        if (response.candidates and 
            len(response.candidates) > 0 and 
            response.candidates[0].content and 
            len(response.candidates[0].content.parts) > 0):
            return response.candidates[0].content.parts[0].text
        else:
            logger.warning(f"Unexpected response structure: {response}")
            return "No response from Gemini."    
    except Exception as e:
        logger.error(f"Error extracting response text: {e}")
        return "Error processing AI response."


def clear_chat_history() -> str:
    """
    Clears the chat history.
    Useful for starting a new conversation or when the context needs to be reset.
    
    Returns:
        str: Confirmation message
    """
    chat_history.clear()
    return "Chat history has been cleared."