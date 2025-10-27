#!/usr/bin/env python3

import subprocess
import sys
import os

def run_command(command, description):
    print(f"Running: {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Success: {description}")
            return True
        else:
            print(f"Failed: {description} - {result.stderr}")
            return False
    except Exception as e:
        print(f"Error during {description}: {e}")
        return False

def main():
    print("WISEACRE Installer started")
    print("Installing required libraries...")
    
    if os.path.exists("requirements.txt"):
        run_command("pip install -r requirements.txt", "Installing from requirements.txt")
    else:
        packages = [
            "python-telegram-bot==20.7",
            "cryptography==41.0.7", 
            "python-dotenv==1.0.0",
            "requests==2.31.0"
        ]
        
        for package in packages:
            if not run_command(f"pip install {package}", f"Installing {package}"):
                print(f"Skipping {package}")
    
    print("Installation completed")

if __name__ == "__main__":
    main()
