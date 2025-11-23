"""
定义 REST API 接口，如 /search
调用 pipeline_runner
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.pipeline_runner import PipelineRunner

router = APIRouter(prefix="/api", tags=["房源助手"])

# 初始化 Pipeline Runner
pipeline_runner = PipelineRunner()


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class SearchResponse(BaseModel):
    results: list
    total: int


@router.post("/search", response_model=SearchResponse)
async def search_properties(request: SearchRequest):
    """
    智能检索房源接口
    
    Args:
        request: 包含查询文本和返回数量
        
    Returns:
        匹配的房源列表
    """
    try:
        results = await pipeline_runner.run_search(request.query, request.top_k)
        return SearchResponse(results=results, total=len(results))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "service": "domus-ai"}
