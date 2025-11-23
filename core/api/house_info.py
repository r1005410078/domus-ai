
"""
core.api.house_info 的 Docstring

房源信息 API 实现，继承自 HouseInfoInterface，提供具体的数据拉取方法
"""

import httpx
from core.interfaces.house_info import HouseInfoInterface
from core.api.http_client import client
from core.models.response_body import ResponseBody

class HouseAPI(HouseInfoInterface):
    def __init__(self, client: httpx.AsyncClient = client):
        self.httpx_client = client
     
    async def fetch_house_data(self, last_updated: str) -> ResponseBody[list[HouseInfoInterface]]:
        """
        拉取房源数据
        :param last_updated: 上次更新时间字符串
        :return: 房源数据列表
        """
        response = await self.httpx_client.get(f"/houses?last_updated={last_updated}")
        response.raise_for_status()
        return response.json()
    
  