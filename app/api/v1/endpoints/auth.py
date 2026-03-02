from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.services.auth_service import AuthService
from app.schemas.base import ResponseModel
from app.schemas.user import UserLoginRequest, LoginResponseData
import jwt
from fastapi import Header, HTTPException, Depends
from sqlmodel import Session
from app.models.user import User
from app.core.config import settings
router = APIRouter()



# 它只负责**参数验证**和**分发任务**
@router.post("/login",response_model=ResponseModel[LoginResponseData])
async def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    service = AuthService()

    # 1. 拿 openid
    openid = await service.get_openid_from_wechat(request.code)
    if not openid:
        raise HTTPException(status_code=400, detail="微信验证失败")

    # 2. 进库操作
    user = service.login_or_register(db, openid)

    # 3. 发令牌
    token = service.create_jwt_token(user.id)

    return ResponseModel(data={
        "token": token,
        "user_info": {
            "nickname": user.nickname,
            "avatar_url": user.avatar_url
        }
    })


def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)) -> User:
    """这是一个依赖注入函数，会自动解析请求头里的 Token"""
    try:
        # 格式通常是 "Bearer <token>"
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="无效 Token")

        user = db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="用户不存在")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="请先登录")