# Flask-Login helpers — stub for future ui/ integration
# Flask calls FastAPI; FastAPI uses srs-auth.
# This module provides decorators for Flask route protection using
# role data stored in the Redis-backed Flask session.

from functools import wraps
from typing import Any

from flask import abort, session


def role_required(*roles: str) -> Any:
    def decorator(f: Any) -> Any:
        @wraps(f)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            user = session.get("user", {})
            if user.get("role") not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated
    return decorator
