"""API2-002 TRUE NEGATIVE: strict algorithm allowlist, no 'none'."""
import jwt

def decode_token(token: str, key: str) -> dict:
    # Explicit allowlist: only RS256 and HS256 accepted
    payload = jwt.decode(token, key, algorithms=["HS256", "RS256"])
    return payload
