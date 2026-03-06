from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Collection(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    wallpaper_id: str = Field(index=True)
    # 为了快速响应，
    thumb_url: Optional[str] = None
    full_res_url: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)