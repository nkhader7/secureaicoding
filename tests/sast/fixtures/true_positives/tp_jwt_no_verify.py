"""API2-001 TRUE POSITIVE: JWT signature verification disabled via keyword arg."""
import jwt

def decode_token(token: str) -> dict:
    # PyJWT >=2.0 keyword form — skips signature verification entirely
    payload = jwt.decode(token, verify_signature=False)
    return payload

def decode_alt(token: str, key: str) -> dict:
    # Options-dict form — same effect, same vulnerability
    opts = {"verify_signature": False, "verify_exp": False}
    return jwt.decode(token, key, algorithms=["HS256"], options=opts)
