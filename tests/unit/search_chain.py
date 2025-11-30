"""
core.nodes.ingestion_node 的 Docstring
数据输入节点，从不同来源拉取或导入数据（MySQL、API、CSV 等），统一接口输出原始数据

"""

import asyncio
from unittest.mock import AsyncMock
from langchain_core.runnables import RunnableConfig
from openai import OpenAI
from core.chains.search_chain import query_house, start_workflows
from pathlib import Path
from core.models.response_body import ResponseBody
from core.models.house_info import HouseInfoModel
import pytest
import json
from qdrant_client import AsyncQdrantClient


@pytest.mark.asyncio
class TestSearchChainNode:

  @pytest.fixture
  def house_api_mock(self):
        mock_api = AsyncMock()
        # 读取json文件作为模拟数据
        file_path = Path(__file__).parent / "../data/mock_house_data.json"
        with open(file_path, "r", encoding="utf-8") as f:
          mock_data = json.load(f)

        mock_data = mock_data.get("data", [])

          # 转成 HouseInfoModel
        house_info = HouseInfoModel(**mock_data)

        # 包装成 ResponseBody
        response = ResponseBody(
          code=200,
          msg="success",
          data=house_info
        )

        mock_api.fetch_house_data.return_value = response
        return mock_api

  # async def test_fetch_house_data(self, house_api_mock):
  #   openai_client = OpenAI(base_url='https://api.openai-proxy.org/v1')
  #   qdrant = AsyncQdrantClient(url="http://localhost:6333")
    
  #   print("开始测试数据拉取")
  #   config = RunnableConfig({
  #     "configurable": {
  #       "openai": openai_client,
  #       "qdrant": qdrant
  #     },
  #     "max_concurrency": 2
  #   })
  #   awork = await start_workflows(api=house_api_mock, config=config)

  async def test_query_house(self, house_api_mock):
    openai_client = OpenAI(base_url='https://api.openai-proxy.org/v1')
    qdrant = AsyncQdrantClient(url="http://localhost:6333")
    config = RunnableConfig({
        "configurable": {
         "openai": openai_client,
         "qdrant": qdrant
      }
    })
    
    res = await query_house(input="回祥 2个房间，有哪些", config=config)
    print(res)



 