from fastapi.routing import APIRouter

from Gainz_App.web.api import assistants, monitoring, users

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(users.router)
api_router.include_router(assistants.router)
