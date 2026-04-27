# srs-auth-service

Standalone authentication utilities for Python.

## Features

- JWT encode/decode (pure Python, PyJWT)
- Password hashing/verification (bcrypt)
- FastAPI dependency factories
- Flask route protection decorator

## Installation

### As a package dependency

```bash
pip install srs-auth-service
```

Or with extras:

```bash
pip install srs-auth-service[fastapi]    # FastAPI dependencies
pip install srs-auth-service[flask]      # Flask-Login
pip install srs-auth-service[dev]        # Development tools (pytest, httpx)
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
├── __init__.py           # Public API exports
├── jwt_utils.py          # create_token, decode_token
├── password.py           # hash_password, verify_password
├── dependencies.py       # FastAPI: make_get_current_user, make_require_role
├── middleware.py         # FastAPI: make_role_guard, make_tenant_guard
└── flask_integration.py  # Flask: role_required decorator
```

## API Reference

### JWT Utilities

```python
from srs_auth import create_token, decode_token

# Create a token
token = create_token(
    payload={"user_id": "123", "role": "buyer"},
    secret_key="your-secret-key",
    expires_in=3600  # seconds, default 1 hour
)

# Decode a token
payload = decode_token(token, secret_key="your-secret-key")
```

### Password Utilities

```python
from srs_auth import hash_password, verify_password

# Hash a password
hashed = hash_password("my-password")

# Verify a password
is_valid = verify_password("my-password", hashed)
```

### FastAPI Integration

```python
from srs_auth.dependencies import make_get_current_user, make_require_role
from srs_auth.middleware import make_role_guard, make_tenant_guard

# Create dependencies
get_current_user = make_get_current_user("your-secret-key")
require_admin = make_require_role("admin", "super_admin")
admin_guard = make_role_guard("your-secret-key", "admin")
tenant_guard = make_tenant_guard("your-secret-key")

# Use in endpoints
@app.get("/me")
async def me(user=Depends(get_current_user)):
    return user

@app.delete("/admin")
async def delete_admin(user=Depends(require_admin)):
    return {"status": "ok"}

@app.get("/orders")
async def list_orders(tenant_id: str, user=Depends(admin_guard)):
    return {"tenant_id": tenant_id, "user": user}
```

### Flask Integration

```python
from srs_auth.flask_integration import role_required

@app.route("/admin")
@role_required("admin", "super_admin")
def admin():
    return {"status": "ok"}
```

## Roles

- `buyer`
- `supplier`
- `admin`
- `super_admin`

## Error Codes

| Code | Meaning |
|------|---------|
| `error.token_expired` | JWT exp claim is in the past |
| `error.invalid_credentials` | Bad or malformed token |
| `error.forbidden` | Role not in allowed set |
| `error.invalid_tenant` | Tenant ID mismatch |

## Development

```bash
# Install dependencies
bash setup-dev.sh
source venv/bin/activate

# Run tests
pytest -v

# Run with coverage
pytest --cov=srs_auth --cov-report=html -v
```

## Publishing

```bash
# Build package
python3 -m build

# Publish to PyPI
twine upload dist/*
```
