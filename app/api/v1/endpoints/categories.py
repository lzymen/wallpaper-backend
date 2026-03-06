from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List
from app.db.session import get_db
from app.models.category import Category
from app.schemas.category import CategoryRead
from app.schemas.base import ResponseModel

router = APIRouter()


@router.get("/", response_model=ResponseModel[List[CategoryRead]])
async def get_categories(db: Session = Depends(get_db)):
    """
    获取全部分类列表：
    1. 只筛选 is_visible=True 的记录
    2. 按照 sort_order 倒序排列（权重高的在前）
    """
    statement = select(Category).where(Category.is_visible == True).order_by(Category.sort_order.desc())
    categories = db.exec(statement).all()

    return ResponseModel(
        data=categories,
        message="success"
    )