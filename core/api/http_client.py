"""
core.api.http_client 的 Docstring
"""

import os
import httpx

# 通过环境变量获取
base_url = os.getenv("API_BASE_URL") or "http://127.0.0.1:9001"

client = httpx.AsyncClient(timeout=10, base_url=base_url)