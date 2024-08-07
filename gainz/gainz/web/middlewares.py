from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException, Depends
from fastapi_users import FastAPIUsers
from gainz.db.models.users import get_user_manager, User
from gainz.web.auth import auth_jwt
from loguru import logger
from fastapi.security import OAuth2PasswordBearer
from fastapi import Security

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/jwt/login")

fastapi_users = FastAPIUsers(get_user_manager, [auth_jwt])


async def get_current_user(token: str = Security(oauth2_scheme)):
    try:
        user = await fastapi_users.get_user(token)
        if user is None:
            raise HTTPException(status_code=403, detail="Not authenticated")
        return user
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(status_code=403, detail="Not authenticated")


class JWTAuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, exclude_routes: list[str] = None):
        super().__init__(app)
        self.exclude_routes = exclude_routes or []

    async def dispatch(self, request: Request, call_next):
        logger.debug(f"Request URL: {request.url.path}")
        logger.debug(f"Request Headers: {request.headers}")

        if request.url.path in self.exclude_routes:
            return await call_next(request)

        try:
            token = request.headers.get("Authorization").split("Bearer ")[1]
            user = await get_current_user(token=token)
            logger.debug(f"Authenticated user: {user}")
            request.state.user = user
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise HTTPException(status_code=403, detail="Not authenticated")

        response = await call_next(request)
        return response
