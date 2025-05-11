from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
# Import utils directly when running from the server directory
from utils import extract_emails_from_url
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    # Redirect to client app
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
    return jsonify({
        'message': 'Welcome to the email extractor API!',
        'usage': {
            'endpoint': '/extract-emails',
            'method': 'POST',
            'body': {
                'url': 'The website URL to crawl',
                'max_pages': '(Optional) Maximum number of pages to crawl (default: 50)'
            },
            'description': 'Extracts emails from an entire website by crawling all pages within the same domain'
        }
    })


@app.route('/extract-emails', methods=['POST'])
def extract_emails():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'message': 'Please provide a valid URL in the request body.'}), 400

    url = data['url']
    max_pages = data.get('max_pages', 50)  # Default to 50 pages if not specified

    result = extract_emails_from_url(url, max_pages=max_pages)
    return jsonify(result)

# Serve frontend files
@app.route('/client/<path:path>')
def serve_client(path):
    # Get the absolute path to the client directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    client_dir = os.path.join(os.path.dirname(current_dir), 'client')
    return send_from_directory(client_dir, path)

@app.route('/client/')
def serve_client_index():
    # Get the absolute path to the client directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    client_dir = os.path.join(os.path.dirname(current_dir), 'client')
    return send_from_directory(client_dir, 'index.html')

if __name__ == '__main__':
    # Use environment variable for port if available (for Render deployment)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

