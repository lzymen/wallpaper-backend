# app/services/wallpaper_service.py
import httpx
from typing import List, Optional
from app.core.config import settings
from app.schemas.wallpaper import WallpaperRead

class WallpaperService:
    def __init__(self):
        # wallhaven api提供的接口地址。
        self.base_url = "https://wallhaven.cc/api/v1/search"
        self.api_key = settings.WALLHAVEN_API_KEY
        self.proxy_url = "http://127.0.0.1:7897"

    # 获取壁纸流服务
    async def get_recommendations(self, user_id: Optional[int] = None) -> List[WallpaperRead]:
        params = {"apikey": self.api_key, "sorting": "random", "purity": "100"}

        async with httpx.AsyncClient(proxy=self.proxy_url) as client:
            try:
                response = await client.get(self.base_url, params=params, timeout=15.0)
                raw_data = response.json().get("data", [])
                print(raw_data)
            except Exception as e:
                print(f"❌ 获取数据失败: {e}")
                return []

        # 其实这个可以封装在外面
        local_ip = "192.168.28.140"
        # 路径必须和 main.py 中的 prefix 以及 router 中的路径完全对应
        proxy_base = f"http://{local_ip}:8000/api/v1/wallpapers/proxy?url="

        clean_list = []
        # 处理封装成前端能理解的类
        for item in raw_data:
            try:
                prepared = {
                    "id": item["id"],
                    "thumb": f"{proxy_base}{item['thumbs']['large']}",
                    "full": f"{proxy_base}{item['path']}",
                    "width": item["dimension_x"],
                    "height": item["dimension_y"]
                }
                clean_list.append(WallpaperRead(**prepared))
            except Exception:
                continue
        return clean_list

    # 获取壁纸详情页方法
    async def get_detail(self, wallpaper_id: str):
        """获取详情并自动包装代理地址"""
        url = f"https://wallhaven.cc/api/v1/w/{wallpaper_id}"
        params = {"api_key": settings.WALLHAVEN_API_KEY}

        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params)
            if resp.status_code != 200:
                return None

            raw_data = resp.json().get("data", {})

            # 原始地址
            original_full = raw_data.get("path")
            original_thumb = raw_data.get("thumbs", {}).get("large")

            # --- 关键：将原始 URL 包装进我们的代理接口 ---
            # 这里的 127.0.0.1:8000 在真机调试时记得改成你电脑的局域网 IP
            proxy_base = "http://127.0.0.1:8000/api/v1/wallpapers/proxy?url="

            return {
                "id": raw_data.get("id"),
                "full_res_url": f"{proxy_base}{original_full}",  # 包装后的原图
                "thumb_url": f"{proxy_base}{original_thumb}",  # 包装后的缩略图
                "resolution": raw_data.get("resolution"),
                "file_type": raw_data.get("file_type"),
                "colors": raw_data.get("colors")
            }