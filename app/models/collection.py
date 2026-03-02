from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Collection(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    wallpaper_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)