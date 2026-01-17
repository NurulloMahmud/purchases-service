from fastapi import APIRouter

from src.api.routes import health

api_router = APIRouter()

# Health checks (no prefix)
api_router.include_router(health.router)

# TODO: Add these in Phase 2
# api_router.include_router(cart.router, prefix="/cart", tags=["Cart"])
# api_router.include_router(checkout.router, prefix="/checkout", tags=["Checkout"])
# api_router.include_router(purchases.router, prefix="/purchases", tags=["Purchases"])
# api_router.include_router(payme_webhook.router, prefix="/payme", tags=["Payme"])
