# app/db/session.py
from sqlmodel import Session, create_engine
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

def get_db():
    # 必须用 sqlmodel 的 Session，
    with Session(engine) as session:
        yield session