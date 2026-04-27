from collections.abc import Callable

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .jwt_utils import decode_token

_bearer = HTTPBearer()


def make_get_current_user(secret_key: str) -> Callable:
    """
    Factory — call once at startup with secret_key, get a FastAPI dependency back.

    Usage in api/app/auth/dependencies.py:
        get_current_user = make_get_current_user(get_settings().secret_key)
    """
    async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    ) -> dict:
        try:
            return decode_token(credentials.credentials, secret_key)
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": "error.token_expired"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": "error.invalid_credentials"},
            )

    return get_current_user


def make_require_role(*roles: str) -> Callable:
    """
    Factory — returns a dependency that enforces role membership.

    Usage:
        require_admin = make_require_role("admin", "super_admin")

        @router.get("/admin/orders")
        async def get_orders(user=Depends(require_admin)):
            ...
    """
    def require_role(user: dict) -> dict:
        if user.get("role") not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "error.forbidden"},
            )
        return user

    return require_role
