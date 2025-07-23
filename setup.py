import subprocess
import os
import sys

def check_python_version():
    """Check if Python version is compatible"""
    required_version = (3, 6)
    current_version = sys.version_info
    
    if current_version < required_version:
        print(f"Error: Python {required_version[0]}.{required_version[1]} or higher is required.")
        print(f"Current version: {current_version[0]}.{current_version[1]}")
        return False
    return True

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("\nPackages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nError installing packages: {e}")
        return False

def check_api_key():
    """Check if API key is set in .env file"""
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    
    if not os.path.exists(env_file):
        print("\nWarning: .env file not found.")
        create_env = input("Would you like to create a .env file now? (y/n): ")
        if create_env.lower() == 'y':
            api_key = input("Enter your Gemini API key: ")
            with open(env_file, "w") as f:
                f.write(f"GEMINI_API_KEY={api_key}")
            print(".env file created successfully!")
            return True
        else:
            print("\nPlease create a .env file with your Gemini API key before running the application.")
            print("Example: GEMINI_API_KEY=your_api_key_here")
            return False
    
    # Check if API key is set in .env file
    with open(env_file, "r") as f:
        content = f.read()
        if "GEMINI_API_KEY=" not in content or "GEMINI_API_KEY=" in content and len(content) < 20:
            print("\nWarning: Gemini API key not found in .env file.")
            update_env = input("Would you like to update your API key now? (y/n): ")
            if update_env.lower() == 'y':
                api_key = input("Enter your Gemini API key: ")
                with open(env_file, "w") as f:
                    f.write(f"GEMINI_API_KEY={api_key}")
                print(".env file updated successfully!")
                return True
            else:
                print("\nPlease update your .env file with a valid Gemini API key before running the application.")
                return False
    
    return True

def main():
    """Main setup function"""
    print("=== Jarvis AI Assistant Setup ===")
    
    if not check_python_version():
        return 1
    
    if not install_requirements():
        return 1
    
    if not check_api_key():
        return 1
    
    print("\n=== Setup Complete! ===")
    print("You can now run the application using:")
    print("  - Command line interface: python main.py")
    print("  - Graphical interface: python gui.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())