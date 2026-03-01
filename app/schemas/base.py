# app/schemas/base.py
from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

# 标准化 API 的响应格式

# 定义一个泛型 T，这样 data 就可以是任何类型（列表、对象等）
T = TypeVar("T")

class ResponseModel(BaseModel, Generic[T]):
    code: int = 200        # 业务状态码
    message: str = "Success" # 提示信息
    data: Optional[T] = None  # 实际的数据内容