from fastapi import APIRouter

router = APIRouter()

from fastapi import APIRouter, Request
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi import Response

#from app.api.deps import get_current_user
from src.app.api.schemas import UserCreate, UserSchema, UserAuth
from src.app.core import security
from src.app.db import crud
from src.app.api.deps import get_current_user

router = APIRouter()

@router.post("/auth", tags=["auth"])
async def login(
    response: Response,
    form_data: UserAuth
):
    user = await security.authenticate_user(
        email=form_data.email, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token, refresh_token = await security.create_tokens(user.email, 
                                                        {"role": user.role})
    response.set_cookie(security.security_config.JWT_ACCESS_COOKIE_NAME, access_token, samesite='strict')
    response.set_cookie(security.security_config.JWT_REFRESH_COOKIE_NAME, refresh_token, samesite='strict')
    return {"detail": "Tokens set in cookies"}

@router.post(
    "/startup",
    #response_model=list[UserSchema],
    #tags=["admin"],
    #dependencies=[Depends(get_current_user)],
)
async def create_tables():
    users = await crud.create_tables()
    return users

@router.get(
    "/",
    response_model=list[UserSchema],
    #tags=["admin"],
    #dependencies=[Depends(get_current_user)],
)
async def read_users(skip: int = 0, limit: int = 100):
    users = await crud.get_users(skip=skip, limit=limit)
    return users

@router.get("/users/me", 
    #response_model=UserSchema, 
    tags=["users"],
    dependencies=[Depends(get_current_user)]
)
def read_users_me(
    request: Request,
    #current_user: dict = Depends(get_current_user)
    #current_user: UserSchema = Depends(get_current_user),
):
    return {"detail": f"{request.state.sub, request.state.role}"}


@router.get("/{user_id}", 
    response_model=UserSchema, 
    #tags=["users"]
)
async def read_user(user_id: int):
    db_user = await crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user

@router.post("/", 
    response_model=UserSchema, 
    #tags=["users"]
)
async def create_user(
    user: UserCreate
):
    db_user = await crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    result = await crud.create_user(user=user)
    return result


@router.delete("/{user_id}", 
    #tags=["admin"]
)
async def remove_user(user_id: int):
    db_user = await crud.get_user(user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    await crud.delete_user(user=db_user)
    return {"detail": f"User with id {user_id} successfully deleted"}
