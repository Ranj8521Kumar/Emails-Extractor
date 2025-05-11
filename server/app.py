from flask import Flask, request, jsonify
from utils import extract_emails_from_url

app = Flask(__name__)

@app.route('/')
def home():
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

if __name__ == '__main__':
    app.run(debug=True)


