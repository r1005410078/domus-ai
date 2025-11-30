"""
Preprocessing Node for HouseModel data.

功能：
1. 清洗 HouseModel，提取结构化字段（rooms/area/price…）
2. 构造 embedding_text 用于语义向量
3. 调用 embedding 模型生成 embedding
4. 输出可直接写入向量数据库的 vector record

依赖：
- pydantic
- openai / or your embedding client
"""
import asyncio
from langchain_core.runnables import Runnable
from typing import List, Optional
from pydantic import BaseModel
import openai
from langchain_core.runnables import RunnableConfig
from core.models.house_info import HouseModel
from qdrant_client.http.models import PointStruct, models

# ==========================
# 输出结构（清洗后的数据）
# ==========================

class HouseCleaned(BaseModel):
    id: str

    # ==== 结构化字段（metadata 用于过滤） ====
    rooms: Optional[int] = None
    halls: Optional[int] = None
    bathrooms: Optional[int] = None
    area: Optional[float] = None
    price: Optional[float] = None

    floor_from: Optional[int] = None
    floor_to: Optional[int] = None

    orientation: Optional[str] = None
    has_elevator: Optional[bool] = None
    near_metro: Optional[bool] = None

    title: Optional[str] = None
    tags: Optional[List[str]] = None

    # ==== embedding 文本 ====
    embedding_text: str

# {
#             "id": str,
#             "embedding": [...],
#             "metadata": {...}
#         }

# ==========================
# Preprocessing Node 主逻辑
# ==========================

class PreprocessingNode(Runnable):
    # 必须实现的属性
    @property
    def InputType(self):
        return HouseModel
    
    @property
    def OutputType(self):
        return PointStruct
    
    def __init__(self, embedding_model: str = "text-embedding-3-large"):
        self.embedding_model = embedding_model

 
    # ==========================
    # Step 1: 清洗 & 结构化提取
    # ==========================
    def clean(self, house: HouseModel) -> HouseCleaned:

        # --- 户型 ---


        apt = house.apartment_type

        rooms = apt and apt.room if apt else None
        halls = apt and apt.hall if apt else None
        bathrooms = apt and apt.bathroom if apt else None

        # --- 面积 ---
        area = house.building_area

        # --- 价格（售优先，其次租） ---
        price = house.sale_price or house.rent_price

        # --- 楼层 ---
        floor_from = house.floor_range.door_number_from if house.floor_range else None
        floor_to = house.floor_range.door_number_to if house.floor_range else None

        # --- 电梯识别 ----
        has_elevator = None
        if house.tags:
            has_elevator = any("电梯" in t for t in house.tags)

        # --- 地铁识别 ---
        text_for_metro = " ".join([
            house.title or "",
            house.remark or "",
            " ".join(house.tags) if house.tags else "",
        ])

        near_metro = True if ("地铁" in text_for_metro or "站" in text_for_metro) else None

        # ==========================
        # 构造 embedding_text
        # ==========================

        embedding_parts = [
            f"id：{house.id or ''}",
            f"标题：{house.title or ''}",
            f"用途：{house.purpose or ''}",
            f"户型：{rooms or ''}室 {halls or ''}厅 {bathrooms or ''}卫",
            f"面积：{area or ''} 平米",
            f"价格：{price or ''}",
            f"楼层：{floor_from or ''}~{floor_to or ''}",
            f"朝向：{house.house_orientation or ''}",
            f"装修：{house.house_decoration or ''}",
            f"标签：{' '.join(house.tags) if house.tags else ''}",
            f"备注：{house.remark or ''}",
        ]

        embedding_text = "；".join([p for p in embedding_parts if p.strip()])

        return HouseCleaned(
            id=house.id or "",
            rooms=rooms,
            halls=halls,
            bathrooms=bathrooms,
            area=area,
            price=price,
            floor_from=floor_from,
            floor_to=floor_to,
            orientation=house.house_orientation,
            has_elevator=has_elevator,
            near_metro=near_metro,
            title=house.title,
            tags=house.tags,
            embedding_text=embedding_text,
        )

    # ==========================
    # Step 2: embedding
    # ==========================
    def embed(self, text: str, config: RunnableConfig) -> List[float]:
        """
        调用 embedding API
        """
        client = config.get("configurable", {}).get("openai")
        assert client is not None, "client 不存在"
        assert isinstance(client, openai.OpenAI), "client 不是 OpenAI 类型"

        resp = client.embeddings.create(
            model=self.embedding_model,
            input=text
        )

        return resp.data[0].embedding
    
       # ---- 主入口 ----
    async def ainvoke(self, input: HouseModel, config: RunnableConfig) -> PointStruct:
        """
        输入 HouseModel
        输出：
        {
            "id": str,
            "embedding": [...],
            "metadata": {...}
        }
        
        """

        print("开始清洗", input.title)
        cleaned = self.clean(input)
        embedding = self.embed(cleaned.embedding_text, config)

        return PointStruct(
            id=cleaned.id,
            vector=embedding,
            payload=cleaned.model_dump(exclude={"embedding_text"})
        )

    def invoke(self, input: HouseModel, config: RunnableConfig) -> PointStruct:
        return asyncio.run(self.ainvoke(input, config))

