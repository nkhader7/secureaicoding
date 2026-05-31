"""API8-001 TRUE NEGATIVE: debug loaded from environment, never hardcoded."""
import os
from flask import Flask

app = Flask(__name__)

# Fail-secure: DEBUG is read from environment; defaults to False
DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
app.config['DEBUG'] = DEBUG

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
