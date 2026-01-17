from fastapi import APIRouter

from src.schemas import MessageResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=MessageResponse)
async def health_check() -> MessageResponse:
    """Health check endpoint."""
    return MessageResponse(message="ok")


@router.get("/ready", response_model=MessageResponse)
async def readiness_check() -> MessageResponse:
    """
    Readiness check endpoint.
    Could be extended to check DB and Redis connections.
    """
    # TODO: Add actual readiness checks (DB, Redis, gRPC)
    return MessageResponse(message="ready")
