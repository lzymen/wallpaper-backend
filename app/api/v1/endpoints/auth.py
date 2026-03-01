from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.services.auth_service import AuthService
from app.schemas.base import ResponseModel

router = APIRouter()


class LoginRequest(BaseModel):
    code: str


@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
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