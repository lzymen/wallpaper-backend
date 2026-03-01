from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

# 创建数据库引擎 [cite: 85]
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# 创建 Session 工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 依赖注入函数：确保每个请求都有独立的数据库连接，处理完自动关闭 [cite: 80, 85]
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()