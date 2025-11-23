"""
core.nodes.ingestion_node 的 Docstring
数据输入节点，从不同来源拉取或导入数据（MySQL、API、CSV 等），统一接口输出原始数据

"""

from unittest.mock import AsyncMock
import pytest

from core.nodes.ingestion_node import Ingestion
import json
from pathlib import Path
from core.models.response_body import ResponseBody
from core.models.house_info import HouseInfoModel

@pytest.mark.asyncio
class TestIngestionNode:

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

        print(house_info)

        # 包装成 ResponseBody
        response = ResponseBody(
          code=200,
          msg="success",
          data=house_info
        )

        mock_api.fetch_house_data.return_value = response
        return mock_api

  async def test_fetch_house_data(self, house_api_mock):
    ingestion_node = Ingestion(house_api=house_api_mock)

    # Mock the API response
    mock_response = house_api_mock.fetch_house_data
    mock_response.return_value = await house_api_mock.fetch_house_data(None, 1, 500)

    houses = await ingestion_node.fetch_house_data()

    assert len(houses) == len(mock_response.return_value.data.list)
    assert houses == mock_response.return_value.data.list

  async def test_run(self, house_api_mock):
    ingestion_node = Ingestion(house_api=house_api_mock)

    # Mock the API response
    mock_response = house_api_mock.fetch_house_data
    mock_response.return_value = await house_api_mock.fetch_house_data(None, 1, 500)

    result = await ingestion_node.run()

    assert result.houses == mock_response.return_value.data.list
    assert result.last_updated == ingestion_node.last_updated