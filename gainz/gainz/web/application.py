from importlib import metadata

from fastapi import FastAPI, Request
from fastapi.responses import UJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from gainz.web.api.router import api_router
from gainz.web.lifespan import lifespan_setup


# Added middleware to resolve CORS issues. 
# To DO: for security, * for all origins, headers, methords are no good. Will be fined tune. 
def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="gainz",
        version=metadata.version("gainz"),
        lifespan=lifespan_setup,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], 
        allow_credentials=True,
        allow_methods=["*"], 
        allow_headers=["*"],  
    )
    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app
