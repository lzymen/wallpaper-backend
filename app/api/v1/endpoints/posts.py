# app/api/v1/endpoints/posts.py
import os
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException,Query
from sqlmodel import Session,select
from sqlalchemy import func
from app.api.v1.endpoints.auth import get_current_user
from app.db.session import get_db
from app.models.post import Post, PostLike
from app.models.user import User
from app.schemas.base import ResponseModel
from app.schemas.post import PostCreate, PostRead, PostListData, PostLikeStatus, PostLikeRequest

router = APIRouter() # ✅ 只保留一个 router 定义


@router.get("/", response_model=ResponseModel[PostListData])
async def get_post_list(
        page: int = Query(1, ge=1, description="页码"),
        limit: int = Query(10, ge=1, le=50, description="每页数量"),
        db: Session = Depends(get_db)
):
    """
    获取社区广场帖子列表
    """
    # 1. 计算分页
    offset = (page - 1) * limit

    # 2. 核心：联表查询 (Join)
    # 我们需要 Post 里的内容 + User 表里的头像/昵称
    # 使用 SQLModel 的 join 语法
    statement = (
        select(Post, User)
        .join(User, Post.user_id == User.id)
        .order_by(Post.created_at.desc())  # 按时间倒序
        .offset(offset)
        .limit(limit)
    )

    # 3. 执行查询
    results = db.exec(statement).all()

    # 4. 获取总数用于前端分页判断
    total_statement = select(func.count()).select_from(Post)
    total = db.exec(total_statement).one()

    # 5. 格式化数据
    final_list = []
    for post, author in results:
        final_list.append(PostRead(
            id=post.id,
            author_name=author.nickname,
            author_avatar=author.avatar_url,
            title=post.title,
            content=post.content,
            images=post.images,  # 数据库 JSON 字段会自动映射为 List
            create_time=post.created_at.strftime("%Y-%m-%d %H:%M"),
            likes_count=post.likes_count,
            comments_count=post.comments_count,
            is_liked=False  # ⚠️ 暂时默认为 False，后续对接点赞表
        ))

    return ResponseModel(data=PostListData(
        total=total,
        page=page,
        list=final_list
    ))




# 基础存储路径
UPLOAD_POST_BASE = "uploads/post"

@router.post("/upload", response_model=ResponseModel[List[str]])
async def upload_post_images(
        files: List[UploadFile] = File(...),
        current_user: User = Depends(get_current_user)
):
    """社区多图上传：按用户名分类存储"""
    user_dir = os.path.join(UPLOAD_POST_BASE, current_user.nickname)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    uploaded_urls = []
    local_ip = "192.168.28.140" # 你的局域网IP

    for file in files:
        ext = os.path.splitext(file.filename)[1]
        unique_name = f"{uuid.uuid4().hex}{ext}"
        file_path = os.path.join(user_dir, unique_name)

        try:
            with open(file_path, "wb") as f:
                f.write(await file.read())
            url = f"http://{local_ip}:8000/uploads/post/{current_user.nickname}/{unique_name}"
            uploaded_urls.append(url)
        except Exception as e:
            print(f"❌ 上传失败: {e}")
            continue

    if not uploaded_urls:
        raise HTTPException(status_code=500, detail="图片上传失败")
    return ResponseModel(data=uploaded_urls)

@router.post("/create", response_model=ResponseModel[PostRead])
async def create_post(
        data: PostCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """保存帖子文本及图片URL"""
    new_post = Post(
        user_id=current_user.id,
        title=data.title,
        content=data.content,
        images=data.images
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    res_data = PostRead(
        id=new_post.id,
        author_name=current_user.nickname,
        author_avatar=current_user.avatar_url,
        title=new_post.title,
        content=new_post.content,
        images=new_post.images,
        create_time=new_post.created_at.strftime("%Y-%m-%d %H:%M"),
        likes_count=0,
        comments_count=0,
        is_liked=False
    )
    return ResponseModel(data=res_data)




@router.post("/like", response_model=ResponseModel[PostLikeStatus])
async def toggle_post_like(
    data: PostLikeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # 必须登录才能点赞
):
    """
    点赞/取消点赞 切换接口
    """
    # 1. 检查帖子是否存在
    post = db.get(Post, data.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="帖子不存在")

    # 2. 检查是否已点赞
    like_query = select(PostLike).where(
        PostLike.user_id == current_user.id,
        PostLike.post_id == data.post_id
    )
    existing_like = db.exec(like_query).first()

    is_liked = False
    if existing_like:
        # 已点赞 -> 取消点赞
        db.delete(existing_like)
        post.likes_count = max(0, post.likes_count - 1) # 防止出现负数
        is_liked = False
    else:
        # 未点赞 -> 新增点赞
        new_like = PostLike(user_id=current_user.id, post_id=data.post_id)
        db.add(new_like)
        post.likes_count += 1
        is_liked = True

    # 3. 提交更改
    db.add(post)
    db.commit()
    db.refresh(post)

    return ResponseModel(data=PostLikeStatus(
        is_liked=is_liked,
        likes_count=post.likes_count
    ))