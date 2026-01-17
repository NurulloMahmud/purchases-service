import grpc

from src.config import get_settings
from src.schemas import AmbassadorValidationResult, ValidAmbassador

# These will be generated from proto file
# Run: python -m grpc_tools.protoc -I./src/grpc_client/proto --python_out=./src/grpc_client --grpc_python_out=./src/grpc_client ./src/grpc_client/proto/ambassador.proto
from src.grpc_client import ambassador_pb2, ambassador_pb2_grpc

settings = get_settings()


class AmbassadorClient:
    """
    gRPC client for communicating with Ambassadors service.
    Validates ambassador IDs and retrieves their prices.
    """

    def __init__(self, address: str | None = None):
        self.address = address or settings.ambassador_grpc_address
        self._channel: grpc.aio.Channel | None = None
        self._stub: ambassador_pb2_grpc.AmbassadorValidationStub | None = None

    async def connect(self) -> None:
        """Establish gRPC channel connection."""
        if self._channel is None:
            self._channel = grpc.aio.insecure_channel(self.address)
            self._stub = ambassador_pb2_grpc.AmbassadorValidationStub(self._channel)

    async def close(self) -> None:
        """Close gRPC channel."""
        if self._channel:
            await self._channel.close()
            self._channel = None
            self._stub = None

    async def validate_ambassadors(
        self, ambassador_ids: list[int]
    ) -> AmbassadorValidationResult:
        """
        Validate a list of ambassador IDs.

        Returns:
            AmbassadorValidationResult with valid ambassadors (id + price) and invalid IDs.

        Raises:
            grpc.RpcError: If gRPC call fails.
        """
        if not self._stub:
            await self.connect()

        request = ambassador_pb2.ValidateRequest(ambassador_ids=ambassador_ids)

        try:
            response = await self._stub.ValidateAmbassadors(request)

            valid_ambassadors = [
                ValidAmbassador(
                    ambassador_id=amb.ambassador_id,
                    price=amb.price,
                )
                for amb in response.valid_ambassadors
            ]

            return AmbassadorValidationResult(
                valid_ambassadors=valid_ambassadors,
                invalid_ids=list(response.invalid_ids),
            )
        except grpc.RpcError as e:
            # Log error and re-raise
            # In production, you might want more sophisticated error handling
            raise


# Singleton instance for dependency injection
_ambassador_client: AmbassadorClient | None = None


async def get_ambassador_client() -> AmbassadorClient:
    """Get or create ambassador gRPC client."""
    global _ambassador_client
    if _ambassador_client is None:
        _ambassador_client = AmbassadorClient()
        await _ambassador_client.connect()
    return _ambassador_client


async def close_ambassador_client() -> None:
    """Close ambassador gRPC client."""
    global _ambassador_client
    if _ambassador_client:
        await _ambassador_client.close()
        _ambassador_client = None
