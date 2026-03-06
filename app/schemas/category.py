from pydantic import BaseModel

class CategoryRead(BaseModel):
    id: int
    name: str
    desc: str
    cover_url: str

    class Config:
        from_attributes = True