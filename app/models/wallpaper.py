# app/models/wallpaper.py
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional


class WallpaperTagLink(SQLModel, table=True):
    """壁纸和标签的多对多中间表"""
    wallpaper_id: Optional[int] = Field(default=None, foreign_key="wallpaper.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)  # 如 "Cyberpunk", "Nature"


class Wallpaper(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    wid: str = Field(unique=True)  # Wallhaven 的原始 ID (如 '9m866e')
    url: str  # 预览图地址
    full_res_url: str  # 原图地址
    width: int
    height: int

    # 建立多对多关联
    tags: List[Tag] = Relationship(link_model=WallpaperTagLink)