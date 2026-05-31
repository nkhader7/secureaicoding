"""API7-001 TRUE NEGATIVE: allowlist enforced before outbound fetch."""
import requests
from urllib.parse import urlparse
from flask import request, jsonify

ALLOWED_HOSTS = {"api.partner.com", "cdn.myapp.com"}

@app.route('/api/fetch-preview', methods=['POST'])
def fetch_preview():
    url = request.json.get('url', '')
    parsed = urlparse(url)
    if parsed.hostname not in ALLOWED_HOSTS or parsed.scheme != 'https':
        return jsonify({'error': 'Disallowed URL'}), 400
    response = requests.get(url, allow_redirects=False, timeout=5)
    return jsonify({'content': response.text})
