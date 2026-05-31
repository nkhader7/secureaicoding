"""API7-001 TRUE POSITIVE: user-controlled URL passed directly to requests.get."""
import requests
from flask import request, jsonify

@app.route('/api/fetch-preview', methods=['POST'])
def fetch_preview():
    # User controls the URL — can reach http://169.254.169.254/latest/meta-data/
    return jsonify({'content': requests.get(request.json.get('url')).text})

@app.route('/api/webhook-test', methods=['POST'])
def webhook_test():
    # req.body.url flows directly into the HTTP call — SSRF
    resp = requests.post(req.body.get('endpoint'), json={'event': 'test'})
    return jsonify({'status': resp.status_code})
