import pytest
from unittest.mock import patch, MagicMock
from core.nodes.preprocessing_node import PreprocessingNode, VectorRecord, HouseCleaned
from core.models.house_info import HouseModel, ApartmentType, FloorRange

# --------------------------
# fixture: 构造一个假的 HouseModel
# --------------------------
@pytest.fixture
def mock_house():
    return HouseModel(
        id="house_123",
        title="南山科技园三房",
        purpose="住宅",
        apartment_type=ApartmentType(room=3, hall=2, bathroom=1),
        building_area=89.5,
        sale_price=3500000,
        floor_range=FloorRange(door_number_from=5, door_number_to=10),
        house_orientation="南",
        house_decoration="精装",
        tags=["学区房", "近地铁", "电梯房"],
        remark="近地铁口，业主急售"
    )


# --------------------------
# 测试 clean(): 清洗逻辑
# --------------------------
def test_clean_function(mock_house):
    node = PreprocessingNode()

    cleaned: HouseCleaned = node.clean(mock_house)

    # 基本字段
    assert cleaned.id == "house_123"
    assert cleaned.rooms == 3
    assert cleaned.halls == 2
    assert cleaned.bathrooms == 1
    assert cleaned.area == 89.5
    assert cleaned.price == 3500000

    assert cleaned.floor_from == 5
    assert cleaned.floor_to == 10

    # 标签识别
    assert cleaned.has_elevator is True
    assert cleaned.near_metro is True

    # embedding_text 不为空
    assert isinstance(cleaned.embedding_text, str)
    assert "南山科技园三房" in cleaned.embedding_text
    assert "89.5" in cleaned.embedding_text
    assert "3500000" in cleaned.embedding_text


# --------------------------
# 测试 process(): 包含 embedding 调用
# 通过 patch mock 掉 openai 请求
# --------------------------
@patch("core.nodes.preprocessing_node.openai.OpenAI")
def test_process_with_mock_embedding(mock_openai, mock_house):
    # mock openai embeddings.create 返回固定 embedding
    mock_client = MagicMock()
    mock_openai.return_value = mock_client

    mock_client.embeddings.create.return_value = MagicMock(
        data=[MagicMock(embedding=[0.1, 0.2, 0.3])]
    )

    node = PreprocessingNode()
    record: VectorRecord = node.process(mock_house)

    # VectorRecord 正确
    assert isinstance(record, VectorRecord)

    # ID 正确
    assert record.id == "house_123"

    # embedding 是 mock 的
    assert record.embedding == [0.1, 0.2, 0.3]

    # metadata 正确
    metadata = record.metadata
    assert metadata["rooms"] == 3
    assert metadata["halls"] == 2
    assert metadata["bathrooms"] == 1
    assert metadata["area"] == 89.5
    assert metadata["price"] == 3500000

    # metadata 中不包含 embedding_text
    assert "embedding_text" not in metadata


# --------------------------
# 测试空字段：确保清洗不会异常
# --------------------------
def test_clean_with_empty_fields():
    empty_house = HouseModel(
        id="empty_1",
        title=None,
        apartment_type=None,
        building_area=None,
        sale_price=None,
        floor_range=None,
        house_orientation=None,
        tags=None,
        remark=None
    )

    node = PreprocessingNode()
    cleaned = node.clean(empty_house)

    assert cleaned.id == "empty_1"
    assert cleaned.rooms is None
    assert cleaned.area is None
    assert isinstance(cleaned.embedding_text, str)

    print(cleaned.embedding_text)
    assert "empty_1" in cleaned.embedding_text