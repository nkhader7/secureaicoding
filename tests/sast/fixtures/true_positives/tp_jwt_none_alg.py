"""API2-002 TRUE POSITIVE: JWT 'none' algorithm accepted."""
import jwt

def decode_token(token: str, key: str) -> dict:
    # Allows unsigned tokens via the 'none' algorithm
    payload = jwt.decode(token, key, algorithms=["HS256", "none"])
    return payload
