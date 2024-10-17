from common_lib.models.settings import FastApiSettings
from common_lib.models.settings import JWTSettings
from common_lib.models.settings import PostgresSettings
from common_lib.models.settings import UvicornSettings
from pydantic import BaseModel

fastapi_settings = FastApiSettings()
uvicorn_settings = UvicornSettings()
postgres_settings = PostgresSettings()
jwt_settings = JWTSettings()


class Settings(BaseModel):
    fastapi_settings: FastApiSettings = fastapi_settings
    uvicorn_settings: UvicornSettings = uvicorn_settings
    postgres_settings: PostgresSettings = postgres_settings
    jwt_settings: JWTSettings = jwt_settings


settings = Settings()
