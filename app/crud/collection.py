from sqlmodel import Session, select
from app.models.collection import Collection

def get_collection(db: Session, user_id: int, wallpaper_id: str):
    statement = select(Collection).where(
        Collection.user_id == user_id,
        Collection.wallpaper_id == wallpaper_id
    )
    return db.exec(statement).first()

def create_collection(db: Session, user_id: int, wallpaper_id: str):
    db_obj = Collection(user_id=user_id, wallpaper_id=wallpaper_id)
    db.add(db_obj)
    db.commit()
    return True

def delete_collection(db: Session, db_obj: Collection):
    db.delete(db_obj)
    db.commit()
    return False

# 根据用户id获取用户在数据库收藏的每个壁纸id
def get_user_collection_ids(db: Session, user_id: int):
    """获取用户收藏的所有壁纸 ID 列表"""
    statement = select(Collection.wallpaper_id).where(Collection.user_id == user_id)
    return db.exec(statement).all()