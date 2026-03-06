from typing import Optional, Union
from fastapi import APIRouter, Depends, HTTPException,status
from sqlmodel import Session,delete
from pydantic import BaseModel
from app.db.session import get_db
from app.models.user import User
from app.schemas.base import ResponseModel
from .auth import get_current_user
from app.schemas.user import UserProfileResponse
from app.schemas.user import ProfileUpdate
from app.models.collection import Collection
router = APIRouter()





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


@router.delete("/account", status_code=status.HTTP_200_OK)
async def delete_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    注销账号接口：
    1. 识别当前用户
    2. 删除该用户所有的收藏记录
    3. 删除该用户自身的账号记录
    """
    try:
        # 步骤 1: 清理收藏记录 (根据 user_id 批量删除)
        # 注意：这里的 user_id 必须与 current_user.id 对应
        stmt_collection = delete(Collection).where(Collection.user_id == current_user.id)
        db.exec(stmt_collection)

        # 步骤 2: 删除用户本人记录
        db.delete(current_user)

        # 步骤 3: 提交事务，确保以上两个动作同时成功
        db.commit()

        return ResponseModel(message="账号已成功注销，相关数据已清理")

    except Exception as e:
        db.rollback() # 出错时回滚，保证数据一致性
        print(f"❌ 注销账号失败: {e}")
        raise HTTPException(status_code=500, detail="注销失败，服务器内部错误")
