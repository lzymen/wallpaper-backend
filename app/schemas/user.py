# app/schemas/user.py
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


class UserProfileResponse(BaseModel):
    nickname: str
    avatar_url: str
    gender: int
    signature: str

    class Config:
        from_attributes = True # 允许直接从数据库模型转换