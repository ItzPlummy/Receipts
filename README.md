# Receipts Test Task

### System requirements

- Python 3.13
- PostgreSQL

## Setup

- Install Poetry
```bash
pip install poetry
```

- Activate the environment
```bash
poetry shell
```

- Fill .env file with required environmental variables
```dotenv
DATABASE_DSN={URL}
TEST_DATABASE_DSN={URL}
JWT_KEY={KEY}
```

- Upgrade migrations
```bash
alembic upgade head
```

## Usage

- Launch FastAPI server
```bash
uvicorn --host 0.0.0.0 --port 8000 --loop asyncio --log-config app/api/v1/logging.json app.asgi:app
```