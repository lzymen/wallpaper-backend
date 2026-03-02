from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.session import get_db
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user  # 鉴权依赖
from app.schemas.collection import CollectionToggle, CollectionStatus
from app.schemas.base import ResponseModel
from app.crud import collection as collection_crud

router = APIRouter()


@router.post("/toggle", response_model=ResponseModel[CollectionStatus])
async def toggle_collection(
        data: CollectionToggle,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)  # 强制登录
):
    """
    点亮或熄灭星星：收藏/取消收藏
    """
    # 1. 检查是否已经收藏过
    existing_collection = collection_crud.get_collection(db, current_user.id, data.wallpaper_id)

    if existing_collection:
        # 2. 如果存在，则删除（取消收藏）
        is_collected = collection_crud.delete_collection(db, existing_collection)
        msg = "已取消收藏"
    else:
        # 3. 如果不存在，则创建（收藏）
        is_collected = collection_crud.create_collection(db, current_user.id, data.wallpaper_id)
        msg = "收藏成功"

    return ResponseModel(data={"is_collected": is_collected}, message=msg)