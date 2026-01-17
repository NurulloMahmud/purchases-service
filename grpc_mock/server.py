"""
Mock gRPC server for Ambassadors service.
Used during development to simulate ambassador validation.

Run with: python -m grpc_mock.server
"""

import asyncio
from concurrent import futures

import grpc

# Import generated proto files
# Run from project root:
# python -m grpc_tools.protoc -I./grpc_mock/proto --python_out=./grpc_mock --grpc_python_out=./grpc_mock ./grpc_mock/proto/ambassador.proto
import ambassador_pb2
import ambassador_pb2_grpc


# Mock database of ambassadors with prices (in tiyin)
MOCK_AMBASSADORS: dict[int, int] = {
    1: 50000_00,    # Ambassador 1: 50,000 UZS
    2: 75000_00,    # Ambassador 2: 75,000 UZS
    3: 100000_00,   # Ambassador 3: 100,000 UZS
    4: 25000_00,    # Ambassador 4: 25,000 UZS
    5: 150000_00,   # Ambassador 5: 150,000 UZS
}


class AmbassadorValidationServicer(ambassador_pb2_grpc.AmbassadorValidationServicer):
    """Mock implementation of AmbassadorValidation service."""

    async def ValidateAmbassadors(
        self,
        request: ambassador_pb2.ValidateRequest,
        context: grpc.aio.ServicerContext,
    ) -> ambassador_pb2.ValidateResponse:
        """Validate ambassador IDs and return prices."""

        valid_ambassadors = []
        invalid_ids = []

        for ambassador_id in request.ambassador_ids:
            if ambassador_id in MOCK_AMBASSADORS:
                valid_ambassadors.append(
                    ambassador_pb2.ValidAmbassador(
                        ambassador_id=ambassador_id,
                        price=MOCK_AMBASSADORS[ambassador_id],
                    )
                )
            else:
                invalid_ids.append(ambassador_id)

        print(f"[Mock gRPC] ValidateAmbassadors called")
        print(f"  Request IDs: {list(request.ambassador_ids)}")
        print(f"  Valid: {[(a.ambassador_id, a.price) for a in valid_ambassadors]}")
        print(f"  Invalid: {invalid_ids}")

        return ambassador_pb2.ValidateResponse(
            valid_ambassadors=valid_ambassadors,
            invalid_ids=invalid_ids,
        )


async def serve(port: int = 50051) -> None:
    """Start the mock gRPC server."""
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    ambassador_pb2_grpc.add_AmbassadorValidationServicer_to_server(
        AmbassadorValidationServicer(), server
    )
    server.add_insecure_port(f"[::]:{port}")

    print(f"[Mock gRPC] Starting server on port {port}")
    print(f"[Mock gRPC] Available ambassadors: {MOCK_AMBASSADORS}")

    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
