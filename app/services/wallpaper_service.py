# app/services/wallpaper_service.py
import asyncio

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

    async def get_batch_details(self, wallpaper_ids: list[str]):
        """并发获取多张壁纸详情，解决搜索接口返回空的问题"""
        if not wallpaper_ids:
            return []

        # 1. 为每个 ID 创建一个任务，调用我们之前写好的 get_detail
        # 这样可以确保每张图都走一遍完整的详情获取逻辑（包含代理包装）
        tasks = [self.get_detail(wid) for wid in wallpaper_ids]

        # 2. 使用 asyncio.gather 同时启动所有请求
        # return_exceptions=True 防止其中一个 ID 挂了导致全部崩溃
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 3. 过滤掉失败的请求（None 或 异常对象）
        valid_results = []
        for res in results:
            if res and isinstance(res, dict):
                # 我们只需要列表页需要的字段，在这里精简一下
                valid_results.append({
                    "id": res.get("id"),
                    "thumb_url": res.get("thumb_url"),
                    "full_res_url": res.get("full_res_url"),
                    "width": int(res.get("resolution", "0x0").split('x')[0]),  # 从 "1920x1080" 提取宽度
                    "height": int(res.get("resolution", "0x0").split('x')[1])  # 提取高度
                })

        return valid_results

    async def get_wallpapers_list(self, query: Optional[str] = None, page: int = 1) -> dict:
        """
        通用获取列表方法：支持关键词搜索和分页
        """
        # 1. 组装参数
        params = {
            "apikey": self.api_key,
            "page": page,
            "purity": "100",  # 只获取 SFW 内容
        }

        # 如果有分类关键词，使用 toplist 排序显得更优质；否则默认随机推荐
        if query:
            params["q"] = query
            params["sorting"] = "toplist"
        else:
            params["sorting"] = "random"

        async with httpx.AsyncClient(proxy=self.proxy_url) as client:
            try:
                # 2. 请求 Wallhaven 接口
                resp = await client.get(self.base_url, params=params, timeout=15.0)
                json_data = resp.json()
                raw_data = json_data.get("data", [])
                meta = json_data.get("meta", {})
            except Exception as e:
                print(f"❌ 搜索数据失败: {e}")
                return {"total": 0, "page": page, "list": []}

        # 3. 包装数据，走图片代理逻辑
        local_ip = "192.168.28.140"
        proxy_base = f"http://{local_ip}:8000/api/v1/wallpapers/proxy?url="

        clean_list = []
        for item in raw_data:
            clean_list.append({
                "id": item["id"],
                "thumb_url": f"{proxy_base}{item['thumbs']['large']}",
                "full_res_url": f"{proxy_base}{item['path']}",
                "width": item["dimension_x"],
                "height": item["dimension_y"]
            })

        return {
            "total": meta.get("total", 0),
            "page": page,
            "list": clean_list
        }