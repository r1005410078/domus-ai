

import asyncio
from langchain_core.runnables import RunnableLambda,  RunnableConfig
from openai import OpenAI
from core.interfaces.house_info import HouseInfoInterface
from core.nodes.filter_node import house_filter_node
from core.nodes.embedding_node import embedding_node
from core.nodes.preprocessing_node import PreprocessingNode
from core.nodes.vectorstore_node import *
from core.nodes.ingestion_node import Ingestion
from config.logging_config import logger

# 异步数据拉取任务
async def data_pull_workflow(api: HouseInfoInterface, config: RunnableConfig):
    while True:
        try:
            logger.info("异步拉取房源数据中...")
            # 1. 拉取数据
            list = await Ingestion(api).ainvoke(None, config)
            # 2. 清洗数据,
            preprocessing_node = PreprocessingNode()
            # 3. 存入数据
            save_node = RunnableLambda(vectorstore_node)

            points =  preprocessing_node | save_node
          
            BATCH_SIZE = 5
            for i in range(0, len(list), BATCH_SIZE):
                batch = list[i:i+BATCH_SIZE]
                # 并发处理这个块内的所有元素
                await asyncio.gather(*[points.ainvoke(item, config) for item in batch])
            
            await asyncio.sleep(60 * 5)  # 每隔 60 秒拉取一次
        except Exception as e:
            print(f"数据拉取异常: {e}")
            await asyncio.sleep(10)

# 异步用户查询任务
async def query_house(input: str, config: RunnableConfig):
    # 1. 接受用户输入数据，将其向量化
    input_node = RunnableLambda(embedding_node)
    # 2. 查询向量数据库
    search_node = RunnableLambda(house_filter_node)
    search_pipeline = input_node | search_node
    return await search_pipeline.ainvoke(input, config)

# 启动异步工作流
async def start_workflows(api: HouseInfoInterface, config: RunnableConfig):
    logger.info("启动异步工作流")
    await asyncio.gather(
        data_pull_workflow(api=api, config=config),
    )


