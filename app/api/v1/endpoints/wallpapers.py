# app/api/v1/endpoints/wallpapers.py
from fastapi import APIRouter, Depends, Query, Response,HTTPException
from typing import List, Optional
import httpx
import secrets
from app.models.category import Category
from app.services.wallpaper_service import WallpaperService
from app.schemas.wallpaper import WallpaperRead, WallpaperDetail, WallpaperData
from app.schemas.base import ResponseModel
from app.db.session import get_db
from app.db.session import Session
from app.utils.translator import translate_zh_to_en

router = APIRouter()

# 接口 1：推荐接口
@router.get("/recommend", response_model=ResponseModel[List[WallpaperRead]])
async def get_wallpapers(
    user_id: Optional[int] = None,
    service: WallpaperService = Depends(WallpaperService)
):
    """获取推荐壁纸"""
    data = await service.get_recommendations(user_id)
    return ResponseModel(data=data)

# 3.分类页面走的接口
@router.get("/classify", response_model=ResponseModel[WallpaperData])
async def get_wallpapers_by_classify(
        category_id: int = Query(..., description="分类ID"),
        page: int = Query(1),
        db: Session = Depends(get_db),
        service: WallpaperService = Depends(WallpaperService)
):
    """专门用于分类页面的瀑布流加载"""
    # 1. 根据 ID 找到分类
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")

    # 2. 拿到英文关键词进行搜索
    search_query = category.desc
    data = await service.get_wallpapers_list(query=search_query, page=page)
    return ResponseModel(data=data)

# 接口 2：代理接口
@router.get("/proxy")
async def image_proxy(url: str = Query(..., description="原始图片地址")):
    """后端图片代理：利用本地代理抓取并转发图片流"""
    # 你的代理软件端口（如 Clash）
    proxies = "http://127.0.0.1:7897"
    headers = {"User-Agent": "Mozilla/5.0"}

    async with httpx.AsyncClient(proxy=proxies, verify=False) as client:
        try:
            resp = await client.get(url, headers=headers, timeout=20.0)
            return Response(
                content=resp.content,
                media_type=resp.headers.get("content-type", "image/jpeg")
            )
        except Exception as e:
            print(f"❌ 代理图片失败: {e}")
            return Response(status_code=404, content="Proxy image error")


@router.get("/search", response_model=ResponseModel[WallpaperData])
async def search_wallpapers(
        q: str = Query(..., description="搜索关键词"),
        page: int = Query(1),
        seed: Optional[str] = Query(None, description="随机种子，第一页留空，后续页带回"),
        service: WallpaperService = Depends(WallpaperService)
):
    """
    专属搜索接口：通过独立的服务方法实现随机瀑布流
    """
    # 1. 翻译词汇
    english_q = await translate_zh_to_en(q)

    # 2. 种子逻辑：如果前端没传 seed（说明是新搜索），我们就生成一个
    # 如果传了 seed（说明在翻页），我们就沿用，保证数据不乱
    current_seed = seed if seed else secrets.token_hex(4)

    # 3. 调用专属的搜索服务方法
    data = await service.search_wallpapers_service(
        query=english_q,
        page=page,
        seed=current_seed
    )

    return ResponseModel(data=data)

@router.get("/{id}", response_model=ResponseModel[WallpaperDetail])
async def get_detail(id: str):
    """根据 ID 获取壁纸详情接口"""
    service = WallpaperService()
    detail = await service.get_detail(id)

    if not detail:
        raise HTTPException(status_code=404, detail="壁纸信息未找到")

    return ResponseModel(data=detail)