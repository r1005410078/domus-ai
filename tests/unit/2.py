import os
from openai import OpenAI

# 设置环境变量
os.environ["OPENAI_API_KEY"] = "sk-..."

# 客户端自动读取环境变量中的 API key
client = OpenAI()

# 调用时指定模型
response = client.chat.completions.create(
    model="gpt-4o-mini",        # ← 指定模型
    messages=[
        {"role": "user", "content": "Hello"}
    ]
)
