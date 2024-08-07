from fastapi import Depends
from fastapi.routing import APIRouter

from gainz.web.api import docs, rabbit, redis, users, openai
from gainz.db.models.users import (
    current_active_user
)

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(
    openai.router, prefix="/openai",
    tags=["openai"], dependencies=[Depends(current_active_user)]
)
api_router.include_router(
    redis.router, prefix="/redis",
    tags=["redis"], dependencies=[Depends(current_active_user)]
)
api_router.include_router(
    rabbit.router, prefix="/rabbit",
    tags=["rabbit"], dependencies=[Depends(current_active_user)]
)
api_router.include_router(docs.router)
