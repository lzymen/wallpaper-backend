import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# 确保是从正确的 endpoints 路径导入
from app.api.v1.endpoints import wallpapers,auth

app = FastAPI(title="WallFlow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(wallpapers.router, prefix="/api/v1/wallpapers", tags=["Wallpapers"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
if __name__ == "__main__":
    # 必须监听 0.0.0.0 才能让局域网内的手机访问
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)