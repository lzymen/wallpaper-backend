# app/models/post.py
from sqlmodel import SQLModel, Field, Column, JSON
from datetime import datetime
from typing import Optional, List

# 帖子表
class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")  # 关联发布者
    title: str = Field(max_length=100)
    content: str = Field(max_length=1000)

    # 存储图片 URL 列表，MySQL 推荐使用 JSON 字段
    images: List[str] = Field(sa_column=Column(JSON))

    likes_count: int = Field(default=0)
    comments_count: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# 点赞表
class PostLike(SQLModel, table=True):
    __tablename__ = "post_like"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    post_id: int = Field(foreign_key="post.id")