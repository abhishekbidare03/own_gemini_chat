import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox, filedialog
import threading
import os
import sys

from chat_logic import chat_with_gemini, clear_chat_history
from error_handler import ErrorHandler, logger

class ChatApp:
    """Main chat application class"""
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.show_welcome_message()
        self.is_processing = False
        
    def send_message(self, event=None):
        """Send user message and get AI response"""
        user_input = self.user_entry.get()
        if not user_input.strip() or self.is_processing:
            return
        
        self.is_processing = True
        
        # Disable input during processing
        self.user_entry.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)
        self.status_label.config(text="Processing...", foreground="#FF6600")
        
        # Display user message
        self.display_message("User", user_input, "user_msg")
        
        # Clear input field
        self.user_entry.delete(0, tk.END)
        
        # Use threading to prevent UI freezing
        threading.Thread(target=self.get_ai_response, args=(user_input,), daemon=True).start()
    
    def get_ai_response(self, user_input):
        """Get AI response in a separate thread"""
        try:
            # Get the AI's response
            ai_response = chat_with_gemini(user_input)
            
            # Display AI response
            self.display_message("Jarvis", ai_response, "ai_msg")
            
        except Exception as e:
            error_msg = ErrorHandler.handle_api_error(e)
            self.display_error(error_msg)
            logger.error(f"Error in get_ai_response: {str(e)}")
        finally:
            # Re-enable input
            self.root.after(0, self.reset_ui_after_response)
    
    def reset_ui_after_response(self):
        """Reset UI elements after response processing"""
        self.user_entry.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)
        self.status_label.config(text="Ready", foreground="black")
        self.user_entry.focus()
        self.is_processing = False
        
    def display_message(self, sender, message, tag):
        """Display a message in the chat window"""
        self.chat_window.config(state=tk.NORMAL)
        
        # Add timestamp if enabled
        if hasattr(self, 'show_timestamp') and self.show_timestamp.get():
            from datetime import datetime
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.chat_window.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Insert the message
        self.chat_window.insert(tk.END, f"{sender}: {message}\n\n", tag)
        self.chat_window.config(state=tk.DISABLED)
        self.chat_window.see(tk.END)
        
    def display_error(self, error_message):
        """Display an error message in the chat window"""
        self.chat_window.config(state=tk.NORMAL)
        self.chat_window.insert(tk.END, f"System: {error_message}\n\n", "error_msg")
        self.chat_window.config(state=tk.DISABLED)
        self.chat_window.see(tk.END)


    def clear_chat(self):
        """Clear the chat window and history"""
        result = messagebox.askyesno("Clear Chat", "Are you sure you want to clear the chat history?")
        if result:
            # Clear the chat window
            self.chat_window.config(state=tk.NORMAL)
            self.chat_window.delete(1.0, tk.END)
            self.chat_window.config(state=tk.DISABLED)
            
            # Clear the chat history in the backend
            message = clear_chat_history()
            
            # Show confirmation
            self.status_label.config(text=message)
            
            # Show welcome message again
            self.show_welcome_message()
    
    def save_chat(self):
        """Save chat history to a text file"""
        if self.chat_window.get(1.0, tk.END).strip() == "":
            messagebox.showinfo("Info", "No chat history to save.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Chat History"
        )
        
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.chat_window.get(1.0, tk.END))
                self.status_label.config(text=f"Chat saved to {os.path.basename(file_path)}")
            except Exception as e:
                ErrorHandler.log_error(e, "Error saving chat history")
                messagebox.showerror("Error", f"Failed to save chat history: {str(e)}")
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        if self.theme_var.get() == "dark":
            # Dark theme
            self.chat_window.config(bg="#2d2d2d", fg="#ffffff")
            self.chat_window.tag_configure("user_msg", foreground="#4da6ff")
            self.chat_window.tag_configure("ai_msg", foreground="#00cc99")
            self.chat_window.tag_configure("error_msg", foreground="#ff6666")
            self.chat_window.tag_configure("timestamp", foreground="#999999")
            self.root.configure(bg="#333333")
            self.main_frame.configure(style="Dark.TFrame")
        else:
            # Light theme
            self.chat_window.config(bg="#f5f5f5", fg="#000000")
            self.chat_window.tag_configure("user_msg", foreground="#003366")
            self.chat_window.tag_configure("ai_msg", foreground="#006633")
            self.chat_window.tag_configure("error_msg", foreground="#cc0000")
            self.chat_window.tag_configure("timestamp", foreground="#666666")
            self.root.configure(bg="#f0f0f0")
            self.main_frame.configure(style="Light.TFrame")
    
    def show_welcome_message(self):
        """Display welcome message in the chat window"""
        welcome_message = "Hi, I am Jarvis. How may I help you?"
        self.display_message("Jarvis", welcome_message, "ai_msg")

    def setup_ui(self):
        """Set up the user interface"""
        # Configure root window
        self.root.title("Jarvis AI Assistant")
        self.root.geometry("700x800")  # Larger initial window size
        self.root.minsize(500, 600)    # Minimum window size
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat")
        self.style.configure("Light.TFrame", background="#f0f0f0")
        self.style.configure("Dark.TFrame", background="#333333")
        
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10 10 10 10", style="Light.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Menu bar
        self.create_menu_bar()
        
        # Chat window with custom tags for styling
        self.chat_window = scrolledtext.ScrolledText(
            self.main_frame, 
            wrap=tk.WORD, 
            state=tk.DISABLED,
            font=("Segoe UI", 10),
            bg="#f5f5f5",
            height=20
        )
        self.chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Configure tags for message styling
        self.chat_window.tag_configure("user_msg", foreground="#003366", font=("Segoe UI", 10, "bold"))
        self.chat_window.tag_configure("ai_msg", foreground="#006633", font=("Segoe UI", 10))
        self.chat_window.tag_configure("error_msg", foreground="#cc0000", font=("Segoe UI", 10, "italic"))
        self.chat_window.tag_configure("timestamp", foreground="#666666", font=("Segoe UI", 8))
        
        # Button frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(padx=10, pady=(0, 10), fill=tk.X)
        
        # Clear button
        self.clear_button = ttk.Button(self.button_frame, text="Clear Chat", command=self.clear_chat)
        self.clear_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Save button
        self.save_button = ttk.Button(self.button_frame, text="Save Chat", command=self.save_chat)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # Theme toggle
        self.theme_var = tk.StringVar(value="light")
        self.theme_check = ttk.Checkbutton(
            self.button_frame, 
            text="Dark Mode", 
            variable=self.theme_var,
            onvalue="dark",
            offvalue="light",
            command=self.toggle_theme
        )
        self.theme_check.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = ttk.Label(self.button_frame, text="Ready")
        self.status_label.pack(side=tk.RIGHT)
        
        # Entry frame
        self.entry_frame = ttk.Frame(self.main_frame)
        self.entry_frame.pack(padx=10, pady=(0, 10), fill=tk.X)
        
        # User input entry
        self.user_entry = ttk.Entry(self.entry_frame, font=("Segoe UI", 10))
        self.user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.user_entry.bind("<Return>", self.send_message)
        self.user_entry.focus()
        
        # Send button
        self.send_button = ttk.Button(self.entry_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)
    
    def create_menu_bar(self):
        """Create the application menu bar"""
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save Chat", command=self.save_chat)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Clear Chat", command=self.clear_chat)
        
        # Preferences submenu
        pref_menu = tk.Menu(edit_menu, tearoff=0)
        
        # Timestamp toggle
        self.show_timestamp = tk.BooleanVar(value=False)
        pref_menu.add_checkbutton(label="Show Timestamps", variable=self.show_timestamp)
        
        edit_menu.add_cascade(label="Preferences", menu=pref_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Jarvis AI Assistant

A Python application that uses Google's Gemini API to create a conversational AI assistant.

Version: 1.0.0

Created with ❤️ using Python and Tkinter."""
        messagebox.showinfo("About Jarvis AI Assistant", about_text)

def main():
    """Main function to start the application"""
    try:
        # Create the root window
        root = tk.Tk()
        
        # Set app icon if available
        try:
            # Look for icon in the same directory as the script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "jarvis_icon.ico")
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
        except Exception as e:
            logger.warning(f"Could not load application icon: {e}")
        
        # Create and start the app
        app = ChatApp(root)
        root.mainloop()
        
    except Exception as e:
        ErrorHandler.log_error(e, "Application startup error")
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()