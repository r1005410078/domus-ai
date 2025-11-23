"""
配置管理类
管理 API Key、模型配置、路径参数等
"""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""
    
    # 项目根目录
    BASE_DIR: Path = Path(__file__).parent.parent
    
    # OpenAI 配置
    OPENAI_API_KEY: str = ""
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    LLM_MODEL: str = "gpt-3.5-turbo"
    
    # 向量库配置
    VECTORSTORE_PATH: str = str(BASE_DIR / "data" / "processed" / "embeddings")
    VECTORSTORE_TYPE: str = "chroma"  # chroma or faiss
    
    # OCR 配置
    OCR_API_URL: str = ""
    OCR_API_KEY: str = ""
    
    # LLM API 配置（如果不使用 OpenAI）
    LLM_API_URL: str = ""
    
    # Redis 配置（可选）
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    # 数据路径
    RAW_DATA_PATH: str = str(BASE_DIR / "data" / "raw")
    PROCESSED_DATA_PATH: str = str(BASE_DIR / "data" / "processed")
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()
