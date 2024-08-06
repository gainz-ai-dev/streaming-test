from fastapi.routing import APIRouter
from gainz.web.api import monitoring

api_router = APIRouter()
api_router.include_router(monitoring.views)
api_router.include_router(monitoring.auth)
api_router.include_router(monitoring.ws)