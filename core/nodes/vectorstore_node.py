"""
core.nodes.vector_dbwrite_node 的 Docstring
向量库管理节点，负责将 embeddings 写入或更新向量数据库
"""

from typing import List
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import PointStruct, models
from langchain_core.runnables import RunnableConfig
  
async def vectorstore_node(input: PointStruct, config: RunnableConfig):
  """
  向量库管理节点，负责将 embeddings 写入或更新向量数据库
  """
  client = config.get("configurable", {}).get("qdrant")
  assert client is not None, "client 不存在"
  assert isinstance(client, AsyncQdrantClient), "client 不是 AsyncQdrantClient 类型"

  if not await client.collection_exists("house_collection"):
    await client.create_collection(
      collection_name="house_collection",
      vectors_config=models.VectorParams(size=3072, distance=models.Distance.COSINE),
    )

  result = await client.upsert(collection_name="house_collection", wait=True, points=[input])
  assert result.status == models.UpdateStatus.COMPLETED

  print("向量库写入成功")

  return {"status": "ok", "count": len([input]), "raw": result}

