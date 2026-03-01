# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = ROOT_DIR / ".env"

# --- 调试代码：运行 main.py 时会在控制台打印这两行 ---
print(f"🔍 架构师正在检查你的 .env 位置...")
print(f"📂 预期路径: {ENV_PATH}")
print(f"❓ 文件是否存在: {ENV_PATH.exists()}")


class Settings(BaseSettings):
    # 增加默认值，这样找不到 .env 也不怕了
    DATABASE_URL: str = "mysql+pymysql://root:root@127.0.0.1:3306/wallflow"
    WALLHAVEN_API_KEY: str = "NJlkGpr0jISmVjNesFdMU3hIrejYlN2T"

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
