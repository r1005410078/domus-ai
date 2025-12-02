
from datetime import datetime
from typing import Optional

from core.interfaces.house_info import HouseInfoInterface
from core.models.house_info import HouseInfoModel
from core.models.response_body import ResponseBody
from config.logging_config import logger
import httpx

http_client = httpx.AsyncClient(timeout=10)

class PullHouseInfoService(HouseInfoInterface):
   async def fetch_house_data(self, last_updated: Optional[datetime], page: int, page_size: int) -> ResponseBody[HouseInfoModel]:
    """
    拉取房源数据
    :param self: 说明
    :return: 房源数据
    """
    
    resp = await http_client.post("http://114.55.227.206:3000/api/domus/query/house/list", data={
      "page": 4,
      "page_size": 100,
      "not_exclude_deleted": True,
      "updated_at": last_updated
    })

    if resp.status_code != 200:
      logger.error("拉取房源数据失败", resp.text)
      raise Exception(resp.text)
    
    return resp.json()
    