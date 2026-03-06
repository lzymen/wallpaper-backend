from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db.session import get_db
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user  # 鉴权依赖
from app.schemas.collection import CollectionToggle, CollectionStatus
from app.schemas.base import ResponseModel
from app.crud import collection as collection_crud
from app.services.wallpaper_service import WallpaperService
from typing import List
from app.schemas.collection import CollectionItem
from app.models.collection import Collection
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
        # 1. 仅在收藏时调一次外部 API
        service = WallpaperService()
        detail = await service.get_detail(data.wallpaper_id)

        # 2. 把查到的详情和用户 ID 一起存进 collection 表
        new_fav = Collection(
            user_id=current_user.id,
            wallpaper_id=data.wallpaper_id,
            thumb_url=detail.get("thumb_url") if detail else "",
            full_res_url=detail.get("full_res_url") if detail else "",
            width=int(detail.get("resolution", "0x0").split('x')[0]) if detail else 0,
            height=int(detail.get("resolution", "0x0").split('x')[1]) if detail else 0
        )
        db.add(new_fav)
        db.commit()
        return ResponseModel(data={"is_collected": True}, message="收藏成功")


@router.get("/list", response_model=ResponseModel[List[CollectionItem]])
async def get_collection_list(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    极速查询：直接读本地 collection 表里的冗余数据
    """
    statement = select(Collection).where(Collection.user_id == current_user.id).order_by(Collection.created_at.desc())
    results = db.exec(statement).all()

    # 此时 results 里已经包含了 thumb_url 等所有信息，直接返回
    collections = []
    for item in results:
        collections.append({
            "id": item.wallpaper_id,  # 👈 这里！把原本的字符串 ID 给到 id 字段
            "thumb_url": item.thumb_url,
            "full_res_url": item.full_res_url,
            "width": item.width,
            "height": item.height
        })
    return ResponseModel(data=collections)