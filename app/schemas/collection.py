from pydantic import BaseModel

class CollectionToggle(BaseModel):
    wallpaper_id: str

class CollectionStatus(BaseModel):
    is_collected: bool