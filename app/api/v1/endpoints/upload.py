from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid
from app.schemas.base import ResponseModel

router = APIRouter()

UPLOAD_DIR = r"E:\Project_Location\Python_Project\wallpaper-backend\uploads"

@router.post("/image", response_model=ResponseModel)
async def upload_image(file: UploadFile = File(...)):
    # 1. 校验文件后缀
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".gif"]:
        raise HTTPException(status_code=400, detail="只允许上传图片(jpg, png, gif)")

    # 2. 生成唯一文件名 (防止重复)
    new_filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, new_filename)

    # 3. 保存文件
    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存失败: {str(e)}")

    # 4. 返回可访问的 URL
    url = f"http://127.0.0.1:8000/uploads/{new_filename}"
    return ResponseModel(data={"url": url})