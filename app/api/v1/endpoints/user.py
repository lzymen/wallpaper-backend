from typing import Optional, Union
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.models.user import User
from app.schemas.base import ResponseModel
from .auth import get_current_user
from app.schemas.user import UserProfileResponse

router = APIRouter()


# 定义前端传参的模具
class ProfileUpdate(BaseModel):
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    # 允许前端传数字，也允许传 None
    gender: Optional[int] = None
    signature: Optional[str] = None


@router.put("/profile")
async def update_profile(
        data: ProfileUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    修改资料接口
    422 报错通常是因为 data 里的字段类型对不上
    """
    try:
        # 更新逻辑
        if data.nickname is not None:
            current_user.nickname = data.nickname
        if data.avatar_url is not None:
            current_user.avatar_url = data.avatar_url
        if data.gender is not None:
            # 确保是整数 0, 1, 2
            current_user.gender = int(data.gender)
        if data.signature is not None:
            current_user.signature = data.signature

        db.add(current_user)
        db.commit()
        db.refresh(current_user)

        return {"code": 200, "message": "修改成功", "data": current_user}

    except Exception as e:
        # 如果报错，打印在后端控制台方便我们查
        print(f"❌ 更新资料失败: {e}")
        raise HTTPException(status_code=500, detail="服务器内部错误")



@router.get("/profile", response_model=ResponseModel[UserProfileResponse])
async def get_profile(current_user: User = Depends(get_current_user)):
    """
    获取当前登录用户的资料
    逻辑：只要 Token 对，current_user 就是从数据库查出来的完整对象
    """
    return ResponseModel(data=current_user)