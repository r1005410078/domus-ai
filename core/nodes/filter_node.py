"""
core.nodes.vector_dbwrite_node 的 Docstring
向量库管理节点，负责将 embeddings 检索接口
"""
from typing import List
from qdrant_client import AsyncQdrantClient
from langchain_core.runnables import RunnableConfig
  
async def house_filter_node(query_vector: List[float], config: RunnableConfig):
  """
  向量库管理节点，负责将 embeddings 检索接口
  """
  
  client = config.get("configurable", {}).get("qdrant")
  assert client is not None, "client 不存在"
  assert isinstance(client, AsyncQdrantClient), "client 不是 AsyncQdrantClient 类型"

  search_result = await client.query_points(
      collection_name="house_collection",
      query=query_vector,
      query_filter=None,
      limit=10
    )

  return search_result

