from typing import Any, Generic, Optional, TypeVar
from anthropic import BaseModel

T = TypeVar("T")  # 泛型参数

class ResponseBody(BaseModel, Generic[T]):
    code: int
    msg: str
    data: T
