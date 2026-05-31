"""API8-001 TRUE POSITIVE: debug mode hardcoded True."""
from flask import Flask

app = Flask(__name__)

# Hardcoded debug exposes full stack traces in 500 responses
DEBUG = True
app.config['DEBUG'] = True

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
