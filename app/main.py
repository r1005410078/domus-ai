

from contextlib import asynccontextmanager
import os
from typing import Annotated
from fastapi import APIRouter, Depends, FastAPI
from openai import OpenAI
from qdrant_client import AsyncQdrantClient
from langchain_core.runnables import RunnableConfig

from config.logging_config import setup_logging
from core.chains.search_chain import query_house, start_workflows
from pydantic import BaseModel

from di.parser_house_info_service import get_parser_house_info_service
from service.parser_house_info import ParserHouseInfoService
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from service.pull_house_info import PullHouseInfoService

QDRANT_DATABASE_URL = os.getenv("QDRANT_DATABASE_URL")
openai_client = OpenAI(base_url='https://api.openai-proxy.org/v1')
qdrant = AsyncQdrantClient(url=QDRANT_DATABASE_URL)

house_api = PullHouseInfoService()

class Query(BaseModel):
    input: str
    

async def job():
    config = RunnableConfig({
      "configurable": {
        "openai": openai_client,
        "qdrant": qdrant
      },
      "max_concurrency": 2
    })
    await start_workflows(api=house_api, config=config)

scheduler =  AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()
    print("应用关闭")

app = FastAPI(lifespan=lifespan)
scheduler.add_job(job, "interval", seconds=5)

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

