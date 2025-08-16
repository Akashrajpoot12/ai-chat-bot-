#!/usr/bin/env python3
"""
Setup script for NLTK data required by the AI ChatBot application.
Run this script once before using the chatbot to download necessary NLTK resources.
"""

import nltk
import sys

def download_nltk_data():
    """Download required NLTK data for the chatbot."""
    print("Setting up NLTK data for AI ChatBot...")
    print("=" * 50)
    
    required_packages = [
        'punkt',      # For sentence tokenization
        'stopwords'   # For stop word removal
    ]
    
    for package in required_packages:
        try:
            print(f"Downloading {package}...")
            nltk.download(package, quiet=True)
            print(f"✓ {package} downloaded successfully")
        except Exception as e:
            print(f"✗ Error downloading {package}: {e}")
            return False
    
    print("\n" + "=" * 50)
    print("✓ NLTK setup completed successfully!")
    print("You can now run the AI ChatBot application.")
    return True

def main():
    """Main function to run the setup."""
    print("AI ChatBot - NLTK Setup")
    print("This script will download required NLTK data for the chatbot to function properly.")
    print()
    
    try:
        success = download_nltk_data()
        if success:
            print("\nSetup completed! You can now run:")
            print("python chatbot_ui.py")
        else:
            print("\nSetup failed. Please check the error messages above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
