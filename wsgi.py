"""
WSGI Entry Point for Email Extractor Application

This module serves as the entry point for WSGI servers (like Gunicorn) to run the application.
It configures the Python path to include the server directory and imports the Flask application.

Author: Your Name
Date: May 2025
"""

import sys
import os

# Add the server directory to the Python path
# This allows the application to be run from different directories
# while still being able to import modules from the server package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'server')))

# Import the Flask application instance
from app import app

# Run the application when this script is executed directly
if __name__ == "__main__":
    app.run()
