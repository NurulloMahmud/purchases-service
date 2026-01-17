FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copy application code
COPY src/ ./src/
COPY migrations/ ./migrations/ 2>/dev/null || true

# Generate gRPC code
COPY src/grpc_client/proto/ ./src/grpc_client/proto/
RUN python -m grpc_tools.protoc \
    -I./src/grpc_client/proto \
    --python_out=./src/grpc_client \
    --grpc_python_out=./src/grpc_client \
    ./src/grpc_client/proto/ambassador.proto

# Fix grpc import path
RUN sed -i 's/import ambassador_pb2/from src.grpc_client import ambassador_pb2/' \
    ./src/grpc_client/ambassador_pb2_grpc.py

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
