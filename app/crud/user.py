from sqlmodel import Session, select
from app.models.user import User
from datetime import datetime

def get_user_by_openid(db: Session, openid: str) -> User:
    """根据 OpenID 查找用户"""
    # 这里的 db 只要是 sqlmodel.Session 就不可能报 exec 错
    statement = select(User).where(User.openid == openid)
    return db.exec(statement).first()

def create_user(db: Session, openid: str) -> User:
    """创建新用户"""
    new_user = User(openid=openid)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user_login(db: Session, user: User) -> User:
    """更新最后登录时间"""
    user.last_login = datetime.utcnow()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user