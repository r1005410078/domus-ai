"""
core.models.house 的 Docstring
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class ApartmentType(BaseModel):
    # 室
    room: Optional[int] = None
    # 厅
    hall: Optional[int] = None
    # 卫
    bathroom: Optional[int] = None
    # 厨
    kitchen: Optional[int] = None
    # 阳台
    terrace: Optional[int] = None
    # 阁楼
    balcony: Optional[int] = None

class ImageInfo(BaseModel):
    name: str
    type: str
    size: str
    url: str

class Stairs(BaseModel):
    stairs: Optional[str] = None
    rooms: Optional[str] = None

class FloorRange(BaseModel):
    door_number_from: Optional[int] = None
    door_number_to: Optional[int] = None

class HouseModel(BaseModel):
    id: Optional[str] = None
    created_by: Optional[str] = None
    community_id: Optional[str] = None
    owner_id: Optional[str] = None
    # 房源标题
    title: Optional[str] = None
    # 用途
    purpose: Optional[str] = None
    # 交易类型
    transaction_type: Optional[str] = None
    # 状态
    house_status: Optional[str] = None
    # 楼层
    floor_range: Optional[FloorRange] = None
    # 地址(楼号/单元号/门牌号)
    house_address: Optional[str] = None
    # 户型
    apartment_type: Optional[ApartmentType] = None
    # 建筑面积
    building_area: Optional[float] = None
    # 装修
    house_decoration: Optional[str] = None
    # 满减年限
    discount_year_limit: Optional[str] = None
    # 梯户
    stairs: Optional[Stairs] = None
    # 推荐标签
    tags: Optional[List[str]] = None
    # 车位高度
    car_height: Optional[float] = None
    # 实率
    actual_rate: Optional[float] = None
    # 级别
    level: Optional[str] = None
    # 层高
    floor_height: Optional[float] = None
    # 进深
    progress_depth: Optional[float] = None
    # 门宽
    door_width: Optional[float] = None
    # 使用面积
    use_area: Optional[float] = None
    # 售价
    sale_price: Optional[float] = None
    # 租价
    rent_price: Optional[float] = None
    # 出租低价
    rent_low_price: Optional[float] = None
    # 首付
    down_payment: Optional[float] = None
    # 出售低价
    sale_low_price: Optional[float] = None
    # 房屋类型
    house_type: Optional[str] = None
    # 朝向
    house_orientation: Optional[str] = None
    # 看房方式
    view_method: Optional[str] = None
    # 付款方式
    payment_method: Optional[str] = None
    # 房源税费
    property_tax: Optional[str] = None
    # 建筑结构
    building_structure: Optional[str] = None
    # 建筑年代
    building_year: Optional[str] = None
    # 产权性质
    property_rights: Optional[str] = None
    # 产权年限
    property_year_limit: Optional[str] = None
    # 产证日期
    certificate_date: Optional[str] = None
    # 交房日期
    handover_date: Optional[str] = None
    # 学位
    degree: Optional[str] = None
    # 户口
    household: Optional[str] = None
    # 来源
    source: Optional[str] = None
    # 委托编号
    delegate_number: Optional[str] = None
    # 唯一住房
    unique_housing: Optional[str] = None
    # 全款
    full_payment: Optional[str] = None
    # 抵押
    mortgage: Optional[str] = None
    # 急切
    urgent: Optional[str] = None
    # 配套
    support: Optional[str] = None
    # 现状
    present_state: Optional[str] = None
    # 外网同步
    external_sync: Optional[str] = None
    # 备注
    remark: Optional[str] = None
    # 房源图片
    images: Optional[List[ImageInfo]] = None
    # 更新时间
    updated_at: Optional[datetime] = None
    # 删除时间
    deleted_at: Optional[datetime] = None

class HouseInfoModel(BaseModel):
    list: List[HouseModel]
    total: int