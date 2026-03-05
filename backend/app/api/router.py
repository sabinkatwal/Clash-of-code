from fastapi import APIRouter

from .routes import auth_router, users_router, matches_router, submissions_router

api_router = APIRouter()

api_router.include_router(auth_router)

api_router.include_router(users_router)

api_router.include_router(matches_router)

api_router.include_router(submissions_router)