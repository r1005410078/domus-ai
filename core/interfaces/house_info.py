"""
core.interfaces.house_info 的 Docstring
房源信息接口，定义获取和处理房源数据的方法
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from core.models.house_info import HouseInfoModel
from core.models.response_body import ResponseBody


class HouseInfoInterface(ABC):

  @abstractmethod
  async def fetch_house_data(self, last_updated: Optional[datetime], page: int, page_size: int) -> ResponseBody[HouseInfoModel]:
    """
    拉取房源数据
    :param self: 说明
    :return: 房源数据
    """
    pass