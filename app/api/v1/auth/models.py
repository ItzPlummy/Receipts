from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr, ConfigDict


class RegisterCredentialsModel(BaseModel):
    username: str = Field(min_length=6, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)


class AuthenticationModel(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: str

    created_at: datetime
    updated_at: datetime | None = None
