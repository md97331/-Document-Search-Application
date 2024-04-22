#!/bin/bash

# Variables
HOST="localhost"
PORT="5000"

# Function to print messages in color
echo_message() {
    echo -e "\033[0;32m$1\033[0m"  # Green color
}

# Ensure the script is run from the correct directory
if [ ! -f "app.py" ]; then
    echo_message "Error: Cannot find 'app.py' in the current directory. Please run this script from the 'CS429-Project' directory."
    exit 1
fi

# Install the required Python dependencies
echo_message "Installing Python dependencies..."
pip install -r requirements.txt

# Run the Flask application
echo_message "Starting the Flask web server..."
FLASK_APP=app.py flask run --host=${HOST} --port=${PORT} &

# Wait for the server to start
sleep 3

# Open the default web browser and navigate to the Flask application
echo_message "Attempting to open the web browser..."
if command -v xdg-open &> /dev/null; then
    xdg-open "http://${HOST}:${PORT}"
else
    echo_message "xdg-open command not found. Please open your web browser manually and navigate to http://${HOST}:${PORT}"
fi

echo_message "The Flask application is now running."
echo_message "Navigate to http://${HOST}:${PORT} in your web browser to access it."
echo_message "Press Ctrl+C to stop the server."

# The script will wait here, keeping the server running until you press Ctrl+C
wait
