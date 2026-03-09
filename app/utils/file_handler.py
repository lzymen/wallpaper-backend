
import os

def get_user_post_dir(username: str):
    """根据用户名获取/创建图片存储目录"""
    base_dir = "uploads/post"
    user_dir = os.path.join(base_dir, username)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    return user_dir