import httpx
import jwt
from datetime import datetime, timedelta
from sqlmodel import Session
from app.core.config import settings
from app.models.user import User
from app.crud import user as user_crud  # 显式导入


class AuthService:
    def __init__(self):
        self.code2session_url = "https://api.weixin.qq.com/sns/jscode2session"

    async def get_openid_from_wechat(self, code: str):
        """去微信服务器换 OpenID"""
        params = {
            "appid": settings.WX_APPID,
            "secret": settings.WX_SECRET,
            "js_code": code,
            "grant_type": "authorization_code"
        }
        async with httpx.AsyncClient() as client:
            try:
                # 如果你后端访问微信也超时，记得在这里加 proxies 参数
                resp = await client.get(self.code2session_url, params=params, timeout=10.0)
                data = resp.json()
                if "openid" not in data:
                    print(f"微信返回错误: {data}")
                return data.get("openid")
            except Exception as e:
                print(f"请求微信异常: {e}")
                return None

    def create_jwt_token(self, user_id: int) -> str:
        """生成登录令牌"""
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode = {"exp": expire, "sub": str(user_id)}
        return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    def login_or_register(self, db: Session, openid: str) -> User:
        """登录注册逻辑"""
        # 调用我们刚写好的 crud
        user = user_crud.get_user_by_openid(db, openid)

        if user:
            # 老用户更新时间
            user = user_crud.update_user_login(db, user)
        else:
            # 新用户直接创建
            user = user_crud.create_user(db, openid)

        return user