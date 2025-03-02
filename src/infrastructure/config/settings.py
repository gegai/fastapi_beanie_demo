from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""
    # MongoDB配置
    mongodb_url: str = "mongodb://admin:Abcd1234@localhost:27017/user_management?authSource=admin"
    database_name: str = "user_management"

    # 服务配置
    app_name: str = "User Management API"
    app_description: str = "User Management API using FastAPI, MongoDB and Beanie"
    app_version: str = "1.0.0"
    debug: bool = False

    # API配置
    api_prefix: str = "/api"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"

    # CORS配置
    allow_origins: list = ["*"]
    allow_credentials: bool = True
    allow_methods: list = ["*"]
    allow_headers: list = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False  # 环境变量名不区分大小写

        # 环境变量前缀
        env_prefix = "APP_"  # 使用APP_作为环境变量前缀，例如APP_MONGODB_URL


settings = Settings()
