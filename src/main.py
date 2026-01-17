from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise import Tortoise

from src.api.routes import api_router
from src.config import TORTOISE_ORM, get_settings
from src.grpc_client import close_ambassador_client

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    - Startup: Initialize DB connection, gRPC client
    - Shutdown: Close connections gracefully
    """
    # Startup
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

    # TODO: Initialize Redis subscriber for ambassador.deleted events

    yield

    # Shutdown
    await close_ambassador_client()
    await Tortoise.close_connections()


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
    )

    app.include_router(api_router)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
