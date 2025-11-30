

from typing import Annotated
from fastapi import Depends
from langchain_openai import ChatOpenAI

from di.ai_provider import get_gpt_4o_mini_client
from service.parser_house_info import ParserHouseInfoService

def get_parser_house_info_service(model: Annotated[ChatOpenAI, Depends(get_gpt_4o_mini_client)]):
  return ParserHouseInfoService(model)
  