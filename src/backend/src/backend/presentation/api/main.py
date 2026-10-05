from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from .dependencies import get_database
from .error_handlers import register_error_handlers
from .routers import auth


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    yield
    get_database().dispose()  # closes the connection pool on shutdown


def create_app() -> FastAPI:
    app = FastAPI(title="AI Foundry", lifespan=lifespan)
    register_error_handlers(app)
    app.include_router(auth.router)
    return app


app = create_app()