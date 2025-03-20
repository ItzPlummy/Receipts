from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from config import Config

config: Config = Config(_env_file=".env")


app = FastAPI(title="Receipts")

app.state.config = config


@app.exception_handler(Exception)
async def on_server_error(request: Request, exception: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal Server Error"}
    )
