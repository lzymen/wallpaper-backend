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