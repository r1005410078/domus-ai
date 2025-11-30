"""
core.nodes.embedding_node 的 Docstring
文本/数据向量化节点，将清洗后的数据生成 embeddings
（基于预训练模型或自定义模型），以便后续相似度计算和检索
"""

from openai import OpenAI
from langchain_core.runnables import RunnableConfig

async def embedding_node(query_str: str, config: RunnableConfig):
  """
  节点入口：接收清洗和 embedding 完成后的数据
  """

  client = config.get("configurable", {}).get("openai")
  assert client is not None, "client 不存在"
  assert isinstance(client, OpenAI), "client 不是 OpenAI 类型"

    # 生成向量
  resp = client.embeddings.create(
      model="text-embedding-3-large",
      input=query_str
  )

  return resp.data[0].embedding