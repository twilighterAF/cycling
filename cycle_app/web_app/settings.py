from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = '0.0.0.0'
    server_port: int = 5000


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
