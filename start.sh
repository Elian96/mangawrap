#!/bin/bash

# Install Playwright browsers (Chromium)
echo "Installing Playwright browser dependencies..."
python -m playwright install chromium

# Start Flask
echo "Starting Flask app..."
python app.py