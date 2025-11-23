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

from typing import List, Optional
from pydantic import BaseModel
import openai

from core.models.house_info import HouseModel


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
class VectorRecord(BaseModel):
    id: str
    embedding: List[float]
    metadata: dict

# ==========================
# Preprocessing Node 主逻辑
# ==========================

class PreprocessingNode:

    def __init__(self, embedding_model: str = "text-embedding-3-large"):
        self.embedding_model = embedding_model

    # ---- 主入口 ----
    def process(self, house: HouseModel) -> VectorRecord:
        """
        输入 HouseModel
        输出：
        {
            "id": str,
            "embedding": [...],
            "metadata": {...}
        }
        """
        cleaned = self.clean(house)
        embedding = self.embed(cleaned.embedding_text)

        return VectorRecord(
            id=cleaned.id,
            embedding=embedding,
            metadata=cleaned.model_dump(exclude={"embedding_text"})
        )

    # ==========================
    # Step 1: 清洗 & 结构化提取
    # ==========================
    def clean(self, house: HouseModel) -> HouseCleaned:

        # --- 户型 ---
        apt = house.apartment_type
        rooms = apt.room if apt else None
        halls = apt.hall if apt else None
        bathrooms = apt.bathroom if apt else None

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
    def embed(self, text: str) -> List[float]:
        """
        调用 embedding API
        """
        client = openai.OpenAI()

        resp = client.embeddings.create(
            model=self.embedding_model,
            input=text
        )

        return resp.data[0].embedding


# ==========================
# 批处理函数（可选）
# ==========================

def preprocess_houses(houses: List[HouseModel], embedding_model: str = "text-embedding-3-large") -> List[VectorRecord]:
    """
    批量清洗 & embedding
    返回用于向量数据库写入的 list
    """
    node = PreprocessingNode(embedding_model)

    results = []
    for h in houses:
        results.append(node.process(h))

    return results