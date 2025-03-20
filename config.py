from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    database_dsn: SecretStr
    test_database_dsn: SecretStr | None = None

    jwt_key: SecretStr
    jwt_algorithm: str = "HS256"
