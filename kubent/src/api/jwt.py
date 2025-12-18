import base64
import jwt
import uuid
from fastapi import Header, HTTPException
from jwt import ExpiredSignatureError, PyJWTError
SECRET_BASE64 = "aitraceinitialsecaitraceinitialsecretaitraceinitialsecretaitraceinitialsecretaitraceinitialsecretaitraceinitialsecretaitraceinitialsecretret"

def verify_at_token(
    at_token: str = Header(...),
) -> uuid.UUID:
    try:
        payload = jwt.decode(
            at_token,
            base64.b64decode(SECRET_BASE64),
            algorithms=["HS256"],
        )
        return uuid.UUID(payload["sub"])

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="AT-token is expired.")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="AT-token invalid.")
