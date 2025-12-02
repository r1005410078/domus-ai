

from typing import Annotated
from fastapi import APIRouter, Depends, FastAPI
from openai import OpenAI
from qdrant_client import AsyncQdrantClient
from langchain_core.runnables import RunnableConfig

from core.chains.search_chain import query_house
from pydantic import BaseModel

from di.parser_house_info_service import get_parser_house_info_service
from service.parser_house_info import ParserHouseInfoService

class Query(BaseModel):
    input: str

app = FastAPI()

openai_client = OpenAI(base_url='https://api.openai-proxy.org/v1')
qdrant = AsyncQdrantClient(url="http://localhost:6333")

config = RunnableConfig({
    "configurable": {
        "openai": openai_client,
        "qdrant": qdrant
    }
})

@app.post("/query_house")
async def query_house_api(query: Query):
    res = await query_house(input=query.input, config=config)
    return { "data": res, "status": "ok", "code": 200 }

@app.post("/ocr")
async def ocr(image_path: str):
    # TODO: 实现 OCR Pipeline
    raise NotImplementedError("OCR Pipeline 待实现")

# 解析房源信息文本输出结构体
@app.post("/parse_text_to_house_info")
async def parse_api(text: str, service: Annotated[ParserHouseInfoService, Depends(get_parser_house_info_service)]):
   res = await service.parse_house_info(text)
   return res

@app.get("/")
async def root():
    return {"message": "这是一个AI房源智能助手服务"}