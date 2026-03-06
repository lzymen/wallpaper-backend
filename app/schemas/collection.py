from pydantic import BaseModel
from pydantic import BaseModel
from typing import List

class CollectionToggle(BaseModel):
    wallpaper_id: str

class CollectionStatus(BaseModel):
    is_collected: bool


class CollectionItem(BaseModel):
    id: str
    thumb_url: str
    full_res_url: str
    width: int
    height: int