from pydantic import BaseModel
from typing import List, Optional
# 壁纸流
class WallpaperRead(BaseModel):
    """
    前端需要的壁纸数据契约
    """
    id: str
    thumb: str
    full: str
    width: int
    height: int

    model_config = {
        "from_attributes": True
    }


class WallpaperDetail(BaseModel):
    id: str
    full_res_url: str
    thumb_url: str
    resolution: str
    file_type: str
    colors: List[str]




# 分类界面规定
class WallpaperItem(BaseModel):
    id: str
    thumb_url: str
    full_res_url: str
    width: int
    height: int

class WallpaperData(BaseModel):
    total: int
    page: int
    list: List[WallpaperItem]