import os
import sys
from datetime import datetime

from chat_logic import chat_with_gemini, clear_chat_history
from error_handler import ErrorHandler, logger

# Try to import readline for command history (available on Unix systems)
try:
    import readline
    READLINE_AVAILABLE = True
except ImportError:
    READLINE_AVAILABLE = False
    logger.info("readline module not available - command history disabled")

class CommandHandler:
    """Handle command-line commands and interactions"""
    
    COMMANDS = {
        "/help": "Show this help message",
        "/clear": "Clear chat history",
        "/save": "Save chat history to a file",
        "/exit": "Exit the program (also /quit or bye)"
    }
    
    @staticmethod
    def print_help():
        """Print available commands"""
        print("\n" + "="*50)
        print("Available commands:")
        for cmd, desc in CommandHandler.COMMANDS.items():
            print(f"  {cmd:<10} - {desc}")
        print("="*50 + "\n")

def save_chat_history(chat_log):
    """Save chat history to a file"""
    if not chat_log:
        print("Jarvis: No chat history to save.")
        return
    
    # Create a filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_history_{timestamp}.txt"
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(chat_log))
        print(f"Jarvis: Chat history saved to {filename}")
    except Exception as e:
        error_msg = f"Failed to save chat history: {str(e)}"
        ErrorHandler.log_error(e, "Error saving chat history")
        print(f"Jarvis: {error_msg}")

def print_with_timestamp(sender, message):
    """Print a message with a timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {sender}: {message}")
    return f"[{timestamp}] {sender}: {message}"

def main():
    """Main function for the command-line interface"""
    # Store chat history for saving later
    chat_log = []
    
    try:
        # Print welcome banner
        print("\n" + "="*50)
        print("Welcome to Jarvis AI Assistant (Command Line Interface)")
        print("="*50)
        
        # Welcome message
        welcome_msg = "Hi, I am Jarvis. How may I help you?"
        log_entry = print_with_timestamp("Jarvis", welcome_msg)
        chat_log.append(log_entry)
        
        print("Type /help to see available commands.\n")
        
        # Enable command history with up/down arrows if readline is available
        if READLINE_AVAILABLE:
            try:
                readline.parse_and_bind('"\\e[A": previous-history')
                readline.parse_and_bind('"\\e[B": next-history')
            except Exception as e:
                logger.warning(f"Could not configure readline: {e}")
        
        while True:
            try:
                # Prompt the user for input
                user_question = input("User: ")
                
                # Skip empty input
                if not user_question.strip():
                    continue
                
                # Log user input
                log_entry = f"User: {user_question}"
                chat_log.append(log_entry)
                
                # Process commands
                cmd = user_question.lower()
                if cmd in ["/exit", "/quit", "bye", "exit", "quit"]:
                    farewell = "Goodbye!"
                    print(f"Jarvis: {farewell}")
                    chat_log.append(f"Jarvis: {farewell}")
                    break
                    
                elif cmd == "/help":
                    CommandHandler.print_help()
                    continue
                    
                elif cmd == "/clear":
                    message = clear_chat_history()
                    print(f"Jarvis: {message}")
                    chat_log = []  # Also clear local chat log
                    continue
                    
                elif cmd == "/save":
                    save_chat_history(chat_log)
                    continue
                
                # Get response from AI
                response = chat_with_gemini(user_question)
                log_entry = print_with_timestamp("Jarvis", response)
                chat_log.append(log_entry)
                
            except KeyboardInterrupt:
                print("\nJarvis: Interrupted. Goodbye!")
                break
                
            except Exception as e:
                error_msg = ErrorHandler.handle_api_error(e)
                print(f"Jarvis: {error_msg}")
                ErrorHandler.log_error(e, "Error in main loop")
    
    except Exception as e:
        ErrorHandler.log_error(e, "Fatal error in main")
        print(f"Fatal error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        ErrorHandler.log_error(e, "Unhandled exception")
        print(f"Unhandled error: {str(e)}")
        sys.exit(1)

