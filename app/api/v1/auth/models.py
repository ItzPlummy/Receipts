from pydantic import BaseModel, Field, EmailStr


class CredentialsModel(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)


class RegisterCredentialsModel(BaseModel):
    username: str = Field(min_length=6, max_length=20)
    email: EmailStr
    password: str = Field(min_length=8, max_length=50)


class AuthenticationModel(BaseModel):
    access_token: str
    token_type: str = "bearer"
