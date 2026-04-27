from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from .dependencies import make_get_current_user


def make_tenant_guard(secret_key: str) -> Callable:
    """
    Returns a dependency that verifies the JWT user belongs to the expected tenant.

    Usage:
        require_tenant = make_tenant_guard(get_settings().secret_key)

        @router.get("/orders")
        async def list_orders(tenant_id: str, user=Depends(require_tenant)):
            # user["tenant_id"] is guaranteed to match path/query tenant_id
    """
    get_current_user = make_get_current_user(secret_key)

    async def tenant_guard(
        tenant_id: str,
        user: dict = Depends(get_current_user),
    ) -> dict:
        if user.get("tenant_id") != tenant_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "error.invalid_tenant"},
            )
        return user

    return tenant_guard


def make_role_guard(secret_key: str, *roles: str) -> Callable:
    """
    Combines JWT verification + role check in one dependency.

    Usage:
        require_admin = make_role_guard(get_settings().secret_key, "admin", "super_admin")

        @router.delete("/products/{id}")
        async def delete_product(user=Depends(require_admin)):
            ...
    """
    get_current_user = make_get_current_user(secret_key)

    async def role_guard(user: dict = Depends(get_current_user)) -> dict:
        if user.get("role") not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "error.forbidden"},
            )
        return user

    return role_guard
