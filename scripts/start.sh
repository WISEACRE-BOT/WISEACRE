#!/bin/bash

echo "==============================="
echo "   WISEACRE Bot Launcher"
echo "==============================="
echo

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    exit 1
fi

# Check requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "ERROR: requirements.txt not found"
    exit 1
fi

echo "Installing/updating dependencies..."
pip3 install -r requirements.txt

echo "Starting WISEACRE bot..."
python3 bot.py
