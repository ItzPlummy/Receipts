from fastapi import APIRouter

from app.api.v1.auth.router import auth_router
from app.api.v1.receipts.router import receipts_router

v1_router: APIRouter = APIRouter(prefix="/v1")

v1_router.include_router(auth_router)
v1_router.include_router(receipts_router)
