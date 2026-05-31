"""API2-001 TRUE NEGATIVE: JWT verification always on."""
import jwt

SECRET_KEY = "loaded-from-secrets-manager"

def decode_token(token: str) -> dict:
    # Signature verified; only HS256 accepted
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload
