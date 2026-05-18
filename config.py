from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    secret_key: SecretStr
    email_user: str = "oluwalunar.misc@gmail.com"
    resend_api_key : SecretStr

    model_config =  SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8"
    )


settings = Settings()