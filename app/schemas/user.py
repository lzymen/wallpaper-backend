# app/schemas/user.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

# 登录请求（进）
class UserLoginRequest(BaseModel):
    code: str

# 用户简要信息（内嵌）
class UserInfo(BaseModel):
    nickname: str
    avatar_url: str

# 登录响应内容（出）
class LoginResponseData(BaseModel):
    token: str
    user_info: UserInfo


# 定义前端传参的模具
class ProfileUpdate(BaseModel):
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    # 允许前端传数字，也允许传 None
    gender: Optional[int] = None
    signature: Optional[str] = None



class UserProfileResponse(BaseModel):
    id: int
    nickname: str
    avatar_url: str
    gender: int
    signature: str
    last_login: datetime

    class Config:
        from_attributes = True # 允许直接从数据库模型转换