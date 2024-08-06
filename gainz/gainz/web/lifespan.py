from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from gainz.services.redis.lifespan import init_redis, shutdown_redis


@asynccontextmanager
async def lifespan_setup(
    app: FastAPI,
) -> AsyncGenerator[None, None]:  # pragma: no cover

    app.middleware_stack = None
    init_redis(app)
    app.middleware_stack = app.build_middleware_stack()

    yield
    await shutdown_redis(app)
