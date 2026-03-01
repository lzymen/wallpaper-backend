# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = ROOT_DIR / ".env"


class Settings(BaseSettings):
    # 增加默认值，这样找不到 .env 也不怕了
    DATABASE_URL: str = "mysql+pymysql://root:root@127.0.0.1:3306/wallflow"
    WALLHAVEN_API_KEY: str = "NJlkGpr0jISmVjNesFdMU3hIrejYlN2T"
    WX_APPID: str = os.getenv("WX_APPID", "")
    WX_SECRET: str = os.getenv("WX_SECRET", "")
    # JWT 签名密钥（随便写一串随机字符）
    JWT_SECRET: str = "wallflow_secret_key_2026"
    JWT_ALGORITHM: str = "HS256"
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding='utf-8',
        extra='ignore'
    )


# 实例化，这样我们在其他地方直接 import settings 就能用了
settings = Settings()


if __name__ == '__main__':
    print(settings.DATABASE_URL)
    print(settings.WALLHAVEN_API_KEY)
