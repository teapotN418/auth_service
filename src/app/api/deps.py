from fastapi import Depends, HTTPException, status, Request
from src.app.core.security import security_obj

async def require_access(request: Request):
    try:
        payload = await security_obj.access_token_required(request)
        request.state.sub = payload.sub
        request.state.data = payload.model_dump(include="role")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{e}"
        )
    
async def require_fresh_access(request: Request):
    try:
        payload = await security_obj.fresh_token_required(request)
        request.state.sub = payload.sub
        request.state.data = payload.model_dump(include="role")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{e}"
        )

async def require_refresh(request: Request):
    try:
        payload = await security_obj.refresh_token_required(request)
        request.state.sub = payload.sub
        request.state.data = payload.model_dump(include="role")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{e}"
        )

def require_role(required_role: str):
    async def role_checker(request: Request, current_user: dict = Depends(require_access)):
        if current_user.get("role") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Require {required_role} role",
            )
        return current_user
    return role_checker