"""
core.nodes.ingestion_node 的 Docstring
数据输入节点，从不同来源拉取或导入数据（MySQL、API、CSV 等），统一接口输出原始数据

"""
import asyncio
from datetime import datetime
from typing import Optional
from anthropic import BaseModel
from core.interfaces.house_info import HouseInfoInterface
from core.models.house_info import HouseModel
from langchain_core.runnables import Runnable
from langchain_core.runnables import  RunnableConfig

class IngestionModel(BaseModel):
  last_updated: Optional[datetime] = None
  houses: list[HouseModel] = []


class Ingestion(Runnable):
  last_updated: Optional[datetime] = None

  # 必须实现的属性
  @property
  def InputType(self):
      return dict
  
  @property
  def OutputType(self):
      return dict

  def __init__(self, house_api: HouseInfoInterface):
    self.house_api = house_api

  async def fetch_house_data(self) -> list[HouseModel]:
    """
    拉取房源数据
    :param self: 说明
    :return: 房源数据
    """
    
    data = []

    # TODO: 递归拉取所有分页数据
    page = 1
    page_size = 500
    while True:
      response = await self.house_api.fetch_house_data(self.last_updated, page, page_size)
      data.extend(response.data.list)
      
      if response.data and response.data.list:
          self.last_updated = response.data.list[-1].updated_at
      else:
          self.last_updated = None

      if len(response.data.list) < page_size:
        break
      page += 1

    return data

  async def ainvoke(self, input, config: RunnableConfig) -> list[HouseModel]:
    """
    运行数据输入节点
    :param self: 说明
    :return: IngestionModel
    """

    houses = await self.fetch_house_data()
    return houses
  
  async def invoke(self, input, config: RunnableConfig) -> list[HouseModel]:
    return asyncio.run(self.ainvoke(input, config))
  
