# app/schemas/post.py
from pydantic import BaseModel
from typing import List
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    content: str
    images: List[str]

class PostRead(BaseModel):
    id: int
    author_name: str
    author_avatar: str
    title: str
    content: str
    images: List[str]
    create_time: str # 格式化后的时间字符串
    likes_count: int
    comments_count: int
    is_liked: bool = False # 默认为 false


class PostListData(BaseModel):
    total: int
    page: int
    list: List[PostRead]



# 点赞请求体
class PostLikeRequest(BaseModel):
    post_id: int # 对应数据库中的 INT 类型

class PostLikeStatus(BaseModel):
    is_liked: bool
    likes_count: int