from fastapi import Depends, HTTPException, status, Request
from src.app.core.security import security_obj, security_config

async def get_current_user(request: Request):
    try:
        payload = await security_obj.access_token_required(request)
        request.state.sub = payload.sub
        request.state.role = payload.model_dump().get("role")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{e}"
        )

async def get_refresh_token_user(request: Request):
    try:
        payload = await security_obj.refresh_token_required(request)
        request.state.sub = payload.sub
        request.state.role = payload.model_dump().get("role")
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{e}"
        )

def role_required(required_role: str):
    async def role_checker(request: Request, current_user: dict = Depends(get_current_user)):
        if current_user.get("role") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Require {required_role} role",
            )
        return current_user
    return role_checker