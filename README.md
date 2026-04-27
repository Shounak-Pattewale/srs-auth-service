# srs-auth-service

Standalone authentication utilities for Python. Pure Python — no framework dependencies.

## Features

- JWT encode/decode (PyJWT, HS256)
- Password hashing/verification (Argon2id via argon2-cffi)

## Installation

```bash
pip install srs-auth-service
```

### From GitHub

```bash
git clone https://github.com/Shounak-Pattewale/srs-auth-service.git
cd srs-auth-service
bash setup-dev.sh
source venv/bin/activate
```

## Package Structure

```
srs_auth/
├── __init__.py     # Public API: create_token, decode_token, hash_password, verify_password
├── jwt_utils.py    # JWT encode/decode — pure Python
└── password.py     # Argon2id hash/verify — pure Python
```

Framework-specific wrappers (FastAPI dependencies, Flask decorators) belong in the consuming service, not here.

## API Reference

### JWT

```python
from srs_auth import create_token, decode_token

token = create_token(
    payload={"user_id": "123", "role": "buyer", "tenant_id": "t1"},
    secret_key="your-secret-key",
    expires_in=3600  # seconds, default 1 hour
)

payload = decode_token(token, secret_key="your-secret-key")
# raises jwt.ExpiredSignatureError if expired
# raises jwt.InvalidTokenError if tampered or wrong secret
```

### Password

```python
from srs_auth import hash_password, verify_password

hashed = hash_password("my-password")        # Argon2id hash
is_valid = verify_password("my-password", hashed)  # True
```

## Framework Integration

srs-auth-service is framework-agnostic. Each consuming service defines its own wrappers.

### FastAPI example

```python
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from srs_auth import decode_token

bearer = HTTPBearer()

def make_get_current_user(secret_key: str):
    async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer),
    ) -> dict:
        try:
            return decode_token(credentials.credentials, secret_key)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail={"code": "error.token_expired"})
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail={"code": "error.invalid_credentials"})
    return get_current_user
```

### Flask example

```python
from functools import wraps
from flask import session, abort
from srs_auth import decode_token

def auth_required(secret_key: str):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get("Authorization", "").replace("Bearer ", "")
            try:
                session["user"] = decode_token(token, secret_key)
            except Exception:
                abort(401)
            return f(*args, **kwargs)
        return decorated
    return decorator
```

See `test-app/` for full working examples for both frameworks.

## Error Codes (convention)

| Code | When |
|------|------|
| `error.token_expired` | JWT `exp` claim is past |
| `error.invalid_credentials` | Bad or malformed token |
| `error.forbidden` | Role not in allowed set |
| `error.invalid_tenant` | Tenant ID mismatch |

## Development

```bash
bash setup-dev.sh
source venv/bin/activate

pytest -v
pytest --cov=srs_auth --cov-report=html -v  # with coverage
```

## Publishing

```bash
python3 -m build
twine upload dist/*
```
