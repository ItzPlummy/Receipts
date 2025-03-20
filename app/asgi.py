from fastapi import FastAPI
from pydantic import ValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.api.v1.exceptions.api_error import APIError
from app.database.database import Database
from config import Config

config: Config = Config(_env_file=".env")
database: Database = Database.from_dsn(config.database_dsn.get_secret_value())


app = FastAPI(title="Receipts")

app.state.config = config
app.state.database = database


@app.exception_handler(ValidationError)
async def on_validation_error(request: Request, exception: ValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exception.errors()},
    )


@app.exception_handler(APIError)
async def on_http_error(request: Request, exception: APIError) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content={"detail": str(exception)},
    )


@app.exception_handler(Exception)
async def on_server_error(request: Request, exception: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"},
    )
