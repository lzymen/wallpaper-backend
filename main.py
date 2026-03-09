import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# 确保是从正确的 endpoints 路径导入
from app.api.v1.endpoints import wallpapers,auth,user, upload,collection,categories,posts
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="WallFlow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 确保路径存在
upload_path = r"E:\Project_Location\Python_Project\wallpaper-backend\uploads"
if not os.path.exists(upload_path):
    os.makedirs(upload_path)

# 挂载静态目录：访问 http://127.0.0.1:8000/uploads/xxx.jpg 就能看到图
app.mount("/uploads", StaticFiles(directory=upload_path), name="uploads")
# 注册路由
app.include_router(wallpapers.router, prefix="/api/v1/wallpapers", tags=["Wallpapers"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(upload.router, prefix="/api/v1/upload", tags=["Upload"])
app.include_router(user.router, prefix="/api/v1/user", tags=["User Profile"])
app.include_router(collection.router, prefix="/api/v1/collection", tags=["Collection"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(posts.router, prefix="/api/v1/posts", tags=["Community"])

if __name__ == "__main__":
    # 必须监听 0.0.0.0 才能让局域网内的手机访问
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)