from pydantic import BaseModel, EmailStr

class UserAuth(BaseModel):
    email: EmailStr = "test@mail.ru"
    password: str = "12345"

class UserBase(BaseModel):
    email: EmailStr = "test@mail.ru"
    role: str = "user"

class UserCreate(UserBase):
    password: str = "12345"

class UserSchema(UserBase):
    id: int