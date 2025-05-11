"""
Email Extractor API - Flask Backend

This module provides a REST API for extracting email addresses from websites.
It crawls websites and extracts all email addresses found on the pages.

Author: Your Name
Date: May 2025
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # For handling Cross-Origin Resource Sharing
# Import utils directly when running from the server directory
from utils import extract_emails_from_url
import os

# Initialize Flask application
app = Flask(__name__)
# Enable CORS for all routes to allow frontend to communicate with the API
CORS(app)

@app.route('/')
def home():
    """
    Root endpoint that redirects users to the client application.

    Returns:
        HTML: A simple HTML page with auto-redirect to the client app.
    """
    # Return HTML with meta refresh to redirect to the client app
    return """
    <html>
        <head>
            <meta http-equiv="refresh" content="0; url=/client/" />
            <title>Redirecting to Email Extractor</title>
        </head>
        <body>
            <p>Redirecting to the Email Extractor app...</p>
            <p><a href="/client/">Click here if you are not redirected automatically</a></p>
        </body>
    </html>
    """

@app.route('/api')
def api_info():
    """
    API information endpoint that provides documentation about the API.

    Returns:
        JSON: Information about the API endpoints and usage.
    """
    return jsonify({
        'message': 'Welcome to the email extractor API!',
        'usage': {
            'endpoint': '/extract-emails',
            'method': 'POST',
            'body': {
                'url': 'The website URL to crawl',
                'max_pages': '(Optional) Maximum number of pages to crawl (default: 10, max: 20)'
            },
            'description': 'Extracts emails from an entire website by crawling pages within the same domain'
        }
    })

@app.route('/health')
def health_check():
    """
    Health check endpoint for monitoring the API status.

    This endpoint is useful for monitoring tools and deployment platforms
    to verify that the application is running correctly.

    Returns:
        JSON: Status information about the API.
    """
    return jsonify({
        'status': 'ok',
        'message': 'Email Extractor API is running'
    })


@app.route('/extract-emails', methods=['POST'])
def extract_emails():
    """
    Main API endpoint for extracting emails from a website.

    This endpoint accepts a POST request with a JSON body containing
    the URL to crawl and optionally the maximum number of pages to crawl.

    Request body:
        {
            "url": "https://example.com",
            "max_pages": 10  # Optional, defaults to 10
        }

    Returns:
        JSON: A dictionary containing the extracted emails and metadata.
              Example: {
                  "emails": ["example@example.com", "contact@example.com"],
                  "pages_crawled": 5,
                  "base_url": "https://example.com"
              }
    """
    # Parse the JSON request body
    data = request.get_json()

    # Validate the request data
    if not data or 'url' not in data:
        return jsonify({'message': 'Please provide a valid URL in the request body.'}), 400

    # Extract parameters from the request
    url = data['url']
    max_pages = data.get('max_pages', 10)  # Default to 10 pages if not specified

    # Limit max_pages to 20 for performance reasons
    max_pages = min(max_pages, 20)

    # Call the utility function to extract emails
    result = extract_emails_from_url(url, max_pages=max_pages)

    # Return the results as JSON
    return jsonify(result)

# Routes for serving the frontend client application
@app.route('/client/<path:path>')
def serve_client(path):
    """
    Serve static files from the client directory.

    This route handles requests for CSS, JavaScript, images, and other
    static assets from the client application.

    Args:
        path (str): The path to the requested file relative to the client directory.

    Returns:
        Response: The requested file.
    """
    # Get the absolute path to the client directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    client_dir = os.path.join(os.path.dirname(current_dir), 'client')
    return send_from_directory(client_dir, path)

@app.route('/client/')
def serve_client_index():
    """
    Serve the main HTML file of the client application.

    This route is called when users navigate to /client/ and returns
    the index.html file that bootstraps the frontend application.

    Returns:
        Response: The index.html file.
    """
    # Get the absolute path to the client directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    client_dir = os.path.join(os.path.dirname(current_dir), 'client')
    return send_from_directory(client_dir, 'index.html')

# Application entry point
if __name__ == '__main__':
    """
    Start the Flask application when this script is run directly.

    This block is executed when the script is run from the command line,
    but not when it's imported as a module.
    """
    # Use environment variable for port if available (for Render deployment)
    port = int(os.environ.get('PORT', 5000))
    # Run the application on all network interfaces (0.0.0.0)
    # This makes it accessible from other computers on the network
    app.run(host='0.0.0.0', port=port, debug=False)

