# app/api/v1/endpoints/wallpapers.py
from fastapi import APIRouter, Depends, Query, Response,HTTPException
from typing import List, Optional
import httpx
from app.services.wallpaper_service import WallpaperService
from app.schemas.wallpaper import WallpaperRead, WallpaperDetail
from app.schemas.base import ResponseModel

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


@router.get("/{id}", response_model=ResponseModel[WallpaperDetail])
async def get_detail(id: str):
    """根据 ID 获取壁纸详情接口"""
    service = WallpaperService()
    detail = await service.get_detail(id)

    if not detail:
        raise HTTPException(status_code=404, detail="壁纸信息未找到")

    return ResponseModel(data=detail)