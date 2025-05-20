from fastapi import FastAPI

import src.app.api.endpoints as endpoints
#from app.api.endpoints import users
from src.app.core.config import settings

tags_metadata = [
    {"name": "no-auth", "description": "Operathions for everyone"},
    {"name": "auth", "description": "Operations for all authenticated"},
    {"name": "user", "description": "Operations for users"},
    {"name": "admin", "description": "Operations for admins"},
]

app = FastAPI(
    openapi_tags=tags_metadata,
    docs_url="/"
)

app.include_router(endpoints.router, prefix="/users")