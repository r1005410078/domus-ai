from datetime import datetime
from typing import List, Optional
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

class ImageInfo(BaseModel):
    type: str = Field(description="图片类型")
    url: str = Field(description="图片地址")

# 定义提取结构
class HouseModel(BaseModel):
    community_name: Optional[str] =  Field(description="小区名称")
    # 用途
    purpose: Optional[str] = Field(description="用途")
    # 交易类型
    transaction_type: Optional[str] = Field(description="交易类型 （出租｜出售）")
    # 楼号
    house_address: Optional[int] = Field(description="房子地址 - 楼号 - 楼层 - 房号")
    # 建筑面积
    building_area: Optional[float] = Field(description="建筑面积")
    # 装修
    house_decoration: Optional[str] = Field(description="装修")
    # 售价
    sale_price: Optional[float] = Field(description="售价")
    # 租价
    rent_price: Optional[float] = Field(description="租价")
    # 出租低价
    rent_low_price: Optional[float] = Field(description="出租低价")
    # 出售低价
    sale_low_price: Optional[float] = Field(description="出售低价")
    # 朝向
    house_orientation: Optional[str]  = Field(description="朝向")
    # 看房方式
    view_method: Optional[str] = Field(description="看房方式")
    # 付款方式
    payment_method: Optional[str] = Field(description="付款方式")
    # 急切
    urgent: Optional[str] = Field(description="急切")
    # 配套
    support: Optional[str] = Field(description="配套")
    # 其他信息备注
    remark: Optional[str] = Field(description="配套")
    # 几室
    room: Optional[int] = Field(description="几室")
    # 几厅
    hall: Optional[int] = Field(description="几厅")
    # 几卫
    bathroom: Optional[int] = Field(description="几卫")
    # 几厨
    kitchen: Optional[int] = Field(description="几厨")
    # 几个阳台
    terrace: Optional[int] = Field(description="几个阳台")
    # 几个阁楼
    balcony: Optional[int] = Field(description="几个阁楼")
    # 联系方式
    phone: Optional[str] = Field(description="联系方式")
    # 姓名
    name: Optional[str] = Field(description="姓名")
    # 图片
    images: Optional[list[ImageInfo]] = Field(description="图片")


# 创建模型并绑定结构化输出
model = ChatOpenAI(model="gpt-4o-mini", base_url="https://api.openai-proxy.org/v1", api_key=lambda: "sk-mH6M90p4io1JreghOnvnQ5Cq6PqegWW5IxIf9rUnzShoiBI5")

structured_model = model.with_structured_output(HouseModel)

# 提取文本
text = """
 张三 回祥小区 3幢 3单元202室 3室1厅2卫 130平方  1500/月 低价 1300/月 押一付三 不出租只卖 家电有空调洗衣机,大床 飞机户型两房朝南 随时看房 13625564028 
 https://cdn.pixabay.com/photo/2025/11/14/17/32/pool-9957219_1280.jpg, https://cdn.pixabay.com/photo/2025/11/14/17/32/pool-9957219_1280.jpg 
"""


result = structured_model.invoke(f"从文本中提取信息：{text}")

print(result)
