"""
外部服务封装
如 LLM 或 OCR API，含请求和错误处理
"""
import logging
from typing import Dict, Any, Optional
import requests
from config.settings import Settings

logger = logging.getLogger(__name__)


class ExternalAPIClient:
    """外部 API 客户端基类"""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """统一处理 API 响应"""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"API请求失败: {e}")
            raise
        except Exception as e:
            logger.error(f"处理响应时出错: {e}")
            raise


class OCRClient(ExternalAPIClient):
    """OCR 服务客户端"""
    
    def __init__(self):
        settings = Settings()
        super().__init__(
            base_url=settings.OCR_API_URL,
            api_key=settings.OCR_API_KEY
        )
    
    def extract_text(self, image_path: str) -> Dict[str, Any]:
        """
        从图片中提取文字
        
        Args:
            image_path: 图片路径
            
        Returns:
            提取的文字信息
        """
        # TODO: 实现具体的 OCR API 调用
        raise NotImplementedError("OCR API 调用待实现")


class LLMClient(ExternalAPIClient):
    """LLM 服务客户端（如果不使用 LangChain 封装）"""
    
    def __init__(self):
        settings = Settings()
        super().__init__(
            base_url=settings.LLM_API_URL,
            api_key=settings.OPENAI_API_KEY
        )
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        生成文本
        
        Args:
            prompt: 提示词
            **kwargs: 其他参数
            
        Returns:
            生成的文本
        """
        # TODO: 实现具体的 LLM API 调用
        raise NotImplementedError("LLM API 调用待实现")
