from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ============================================================
# JWT / Auth
# ============================================================
class UserClaims(BaseModel):
    """JWT token claims structure matching Go service."""

    id: int
    email: str
    first_name: str | None = None
    last_name: str | None = None
    role: str | None = None
    exp: int


# ============================================================
# Cart
# ============================================================
class CartItemAdd(BaseModel):
    """Request to add an ambassador to cart."""

    ambassador_id: int


class CartItemResponse(BaseModel):
    """Single cart item with price from Ambassadors service."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    ambassador_id: int
    price: int  # tiyin, fetched from Ambassadors
    created_at: datetime


class CartResponse(BaseModel):
    """Full cart with items and total."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    items: list[CartItemResponse]
    total: int  # sum of all prices in tiyin
    created_at: datetime


class CartItemRemove(BaseModel):
    """Request to remove an ambassador from cart."""

    ambassador_id: int


# ============================================================
# Checkout
# ============================================================
class CheckoutResponse(BaseModel):
    """Response after initiating checkout."""

    purchase_id: int
    payment_id: int
    amount: int  # tiyin
    payment_url: str


# ============================================================
# Purchase
# ============================================================
class PurchaseResponse(BaseModel):
    """Single purchase record."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    ambassador_id: int
    price_paid: int
    created_at: datetime


class PurchaseListResponse(BaseModel):
    """List of user's purchases."""

    purchases: list[PurchaseResponse]
    total: int  # count


# ============================================================
# Payment (internal use, Payme webhooks)
# ============================================================
class PaymentResponse(BaseModel):
    """Payment status."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    purchase_id: int
    status: str
    amount: int
    created_at: datetime
    updated_at: datetime


# ============================================================
# gRPC related (for type hints in services)
# ============================================================
class ValidAmbassador(BaseModel):
    """Ambassador data returned from gRPC validation."""

    ambassador_id: int
    price: int  # tiyin


class AmbassadorValidationResult(BaseModel):
    """Result of validating ambassador IDs via gRPC."""

    valid_ambassadors: list[ValidAmbassador]
    invalid_ids: list[int]


# ============================================================
# Generic responses
# ============================================================
class MessageResponse(BaseModel):
    """Generic message response."""

    message: str


class ErrorResponse(BaseModel):
    """Error response."""

    detail: str
