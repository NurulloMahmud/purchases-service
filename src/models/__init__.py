from tortoise import fields
from tortoise.models import Model


class Cart(Model):
    """One cart per user, no expiration."""

    id = fields.BigIntField(primary_key=True)
    user_id = fields.BigIntField(unique=True, index=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    cart_items: fields.ReverseRelation["CartItem"]

    class Meta:
        table = "carts"


class CartItem(Model):
    """Items in a cart. Price is fetched from Ambassadors service on read."""

    id = fields.BigIntField(primary_key=True)
    cart = fields.ForeignKeyField(
        "models.Cart",
        related_name="cart_items",
        on_delete=fields.CASCADE,
    )
    ambassador_id = fields.BigIntField(index=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "cart_items"
        unique_together = (("cart", "ambassador_id"),)


class Purchase(Model):
    """Completed purchases. Stores price at time of purchase."""

    id = fields.BigIntField(primary_key=True)
    user_id = fields.BigIntField(index=True)
    ambassador_id = fields.BigIntField(index=True)
    price_paid = fields.BigIntField()  # in tiyin
    created_at = fields.DatetimeField(auto_now_add=True)

    payment: fields.ForeignKeyRelation["Payment"]

    class Meta:
        table = "purchases"


class PaymentStatus:
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class Payment(Model):
    """
    Payment records linked to purchases.
    One payment per purchase.
    """

    id = fields.BigIntField(primary_key=True)
    transaction_id = fields.CharField(max_length=255, null=True, index=True)  # Payme transaction ID
    purchase = fields.ForeignKeyField(
        "models.Purchase",
        related_name="payment",
        on_delete=fields.CASCADE,
    )
    status = fields.CharField(max_length=20, default=PaymentStatus.PENDING, index=True)
    amount = fields.BigIntField()  # in tiyin

    # Payme specific fields
    payme_transaction_id = fields.CharField(max_length=255, null=True)
    payme_time = fields.BigIntField(null=True)  # Payme timestamp
    payme_state = fields.IntField(null=True)  # Payme transaction state
    payme_reason = fields.IntField(null=True)  # Cancellation reason if any

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "payments"
