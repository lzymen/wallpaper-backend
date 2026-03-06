from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=64)
    desc: Optional[str] = Field(default="", max_length=128)
    cover_url: str = Field(max_length=255)
    sort_order: int = Field(default=0)
    is_visible: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)