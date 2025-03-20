from fastapi import APIRouter

auth_router: APIRouter = APIRouter(prefix="/auth", tags=["Authorization"])
