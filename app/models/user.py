from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    # 物理主键
    id: Optional[int] = Field(default=None, primary_key=True)
    # 微信唯一标识，必须加唯一索引
    openid: str = Field(unique=True, index=True)
    # 用户昵称，设置默认值
    nickname: str = Field(default="壁纸旅客")
    # 头像地址，设置默认占位图
    avatar_url: str = Field(default="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix")
    # 注册时间
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # 最后登录时间
    last_login: datetime = Field(default_factory=datetime.utcnow)