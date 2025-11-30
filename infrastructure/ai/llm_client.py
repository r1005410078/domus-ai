

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()  # 默认读取 .env 文件

gpt_4o_mini_client = ChatOpenAI(model="gpt-4.1-mini", base_url="https://api.openai-proxy.org/v1")