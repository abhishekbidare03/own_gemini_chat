# Jarvis AI Assistant

A Python-based AI assistant that uses Google's Gemini API to provide conversational AI capabilities. The application features both a command-line interface and a graphical user interface.

## Features

- **Conversational AI**: Interact with Google's Gemini AI model
- **Dual Interface**: Use either command-line or graphical interface
- **Chat History**: Maintains conversation context
- **Modern UI**: Clean, responsive graphical interface
- **Error Handling**: Robust error handling and logging

## Requirements

- Python 3.6 or higher
- Google Gemini API key
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone or download this repository
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
   You can get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Usage

### Command-line Interface

Run the following command to start the command-line interface:

```
python main.py
```

Type your messages and press Enter. Type 'exit', 'quit', or 'bye' to end the conversation.

### Graphical User Interface

Run the following command to start the graphical interface:

```
python gui.py
```

The GUI provides a chat window, input field, and buttons for sending messages and clearing chat history.

## Project Structure

- `main.py`: Command-line interface
- `gui.py`: Graphical user interface
- `chat_logic.py`: Core functionality for interacting with the Gemini API
- `.env`: Environment variables (API key)
- `requirements.txt`: Required Python packages

## Features

- **Chat History Management**: Automatically manages chat history length to prevent token limit issues
- **Threading**: UI remains responsive during API calls
- **Safety Settings**: Implements Gemini's safety settings to filter inappropriate content
- **Error Handling**: Comprehensive error handling and logging
- **Modern UI**: Clean, responsive graphical interface with styled messages

## License

This project is open source and available under the MIT License.

## Acknowledgements

- Google Generative AI for the Gemini API
- Python tkinter library for the GUI
