# Purchases Microservice

A FastAPI-based purchases and cart management service with Payme payment integration.

## Architecture

```
┌──────────────────┐                        ┌──────────────────┐
│                  │   gRPC (sync)          │                  │
│    Purchases     │ ────────────────────►  │   Ambassadors    │
│    (FastAPI)     │   ValidateAmbassadors  │   (Go)           │
│                  │ ◄────────────────────  │                  │
└────────┬─────────┘                        └────────┬─────────┘
         │                                           │
         │           ┌─────────────┐                 │
         └──────────►│    Redis    │◄────────────────┘
           subscribe │  pub/sub    │  publish
                     │  + ARQ      │  ambassador.deleted
                     └─────────────┘
```

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL + Tortoise ORM
- **Task Queue**: ARQ (Redis-backed)
- **Inter-service**: gRPC (for validation), Redis pub/sub (for events)
- **Payments**: Payme via paytechuz package

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- (Optional) Make

### Development Setup

1. **Clone and setup environment**

```bash
cp .env.example .env
# Edit .env with your values
```

2. **Start services with Docker Compose**

```bash
docker-compose up -d
```

This starts:
- PostgreSQL (port 5432)
- Redis (port 6379)
- gRPC mock server (port 50051)
- Purchases API (port 8000)
- ARQ worker

3. **Or run locally**

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"

# Generate gRPC code
python -m grpc_tools.protoc \
    -I./src/grpc_client/proto \
    --python_out=./src/grpc_client \
    --grpc_python_out=./src/grpc_client \
    ./src/grpc_client/proto/ambassador.proto

# Run migrations
aerich upgrade

# Start server
uvicorn src.main:app --reload
```

## API Endpoints

### Health
- `GET /health` - Health check
- `GET /ready` - Readiness check

### Cart (requires auth)
- `GET /cart` - Get user's cart with live prices
- `POST /cart/items` - Add ambassador to cart
- `DELETE /cart/items` - Remove ambassador from cart

### Checkout (requires auth)
- `POST /checkout` - Initiate payment, get Payme link

### Purchases (requires auth)
- `GET /purchases` - List user's purchase history

### Payme Webhook
- `POST /payme/webhook` - Payme callback endpoint

## Database Schema

```
carts
├── id (PK)
├── user_id (unique, indexed)
└── created_at

cart_items
├── id (PK)
├── cart_id (FK → carts)
├── ambassador_id (indexed)
└── created_at

purchases
├── id (PK)
├── user_id (indexed)
├── ambassador_id (indexed)
├── price_paid (tiyin)
└── created_at

payments
├── id (PK)
├── transaction_id
├── purchase_id (FK → purchases)
├── status
├── amount (tiyin)
├── payme_* fields
├── created_at
└── updated_at
```

## Configuration

See `.env.example` for all configuration options.

Key settings:
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `AMBASSADOR_GRPC_HOST/PORT` - gRPC server address
- `PAYME_*` - Payme credentials
- `JWT_SECRET` - Must match your auth service

## Testing

```bash
pytest
```

## License

MIT
