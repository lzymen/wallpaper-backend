from pydantic import BaseModel

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