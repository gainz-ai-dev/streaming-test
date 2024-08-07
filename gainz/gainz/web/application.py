from importlib import metadata
from pathlib import Path

from fastapi import FastAPI, WebSocket
from fastapi.responses import UJSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from gainz.log import configure_logging
from gainz.web.api.router import api_router
from gainz.web.lifespan import lifespan_setup
from gainz.services.websocket_service import websocket_endpoint

APP_ROOT = Path(__file__).parent.parent


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="Gainz.ai",
        version=metadata.version("gainz"),
        lifespan=lifespan_setup,
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Add CORS middleware
    origins = [
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    # Adds static directory.
    # This directory is used to access swagger files.
    app.mount("/static", StaticFiles(directory=APP_ROOT / "static"), name="static")

    # app.add_middleware(
    #     JWTAuthenticationMiddleware,
    #     exclude_routes=[
    #         "/auth/register",
    #         "/auth/forgot-password",
    #         "/auth/reset-password",
    #         "/auth/request-verify-token",
    #         "/auth/verify",
    #         "/auth/jwt/login",
    #         "/auth/jwt/logout",
    #         "/auth/jwt/logout",
    #         "/docs",
    #         "/redoc",
    #         "/openapi.json",
    #     ]
    # )

    # WebSocket endpoint
    app.websocket("/ws")(websocket_endpoint)

    return app
