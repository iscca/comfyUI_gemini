"""
Gemini API工具类
"""

import requests
import json
import time
import logging
from typing import Optional, Dict, Any
from config import DEFAULT_CONFIG, EXPANSION_STYLES, TRANSLATION_CONFIG

class GeminiAPIClient:
    """
    Gemini API客户端类
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = DEFAULT_CONFIG["api_base_url"]
        self.timeout = DEFAULT_CONFIG["timeout"]
        self.max_retries = DEFAULT_CONFIG["max_retries"]
        
    def _make_request(self, prompt: str, max_tokens: int = 1000, 
                     temperature: float = 0.7, top_p: float = 0.8, 
                     top_k: int = 40) -> Optional[str]:
        """
        发送API请求
        """
        url = f"{self.base_url}?key={self.api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": temperature,
                "topP": top_p,
                "topK": top_k
            }
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(url, headers=headers, json=data, timeout=self.timeout)
                response.raise_for_status()
                
                result = response.json()
                
                if "candidates" in result and len(result["candidates"]) > 0:
                    content = result["candidates"][0]["content"]["parts"][0]["text"]
                    return content.strip()
                else:
                    logging.warning(f"API返回空内容，尝试 {attempt + 1}/{self.max_retries}")
                    
            except requests.exceptions.Timeout:
                logging.warning(f"请求超时，尝试 {attempt + 1}/{self.max_retries}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                    
            except requests.exceptions.RequestException as e:
                logging.error(f"API请求错误: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    return f"API请求失败: {str(e)}"
                    
            except Exception as e:
                logging.error(f"未知错误: {e}")
                return f"处理错误: {str(e)}"
        
        return "API调用失败：达到最大重试次数"
    
    def expand_text(self, text: str, style: str = "详细描述", max_tokens: int = 1000) -> str:
        """
        扩写文本
        """
        style_config = EXPANSION_STYLES.get(style, EXPANSION_STYLES["详细描述"])
        prompt = f"{style_config['prompt_prefix']}\n\n{text}\n\n请保持原文的核心意思，但要大幅增加内容的丰富度和表现力。"
        
        return self._make_request(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=style_config.get("temperature", DEFAULT_CONFIG["default_temperature"])
        )
    
    def translate_to_english(self, text: str, max_tokens: int = 1000) -> str:
        """
        翻译为英文
        """
        prompt = TRANSLATION_CONFIG["prompt_template"].format(text=text)
        
        return self._make_request(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=TRANSLATION_CONFIG["temperature"]
        )

class TextProcessor:
    """
    文本处理器类
    """
    
    def __init__(self, api_key: str):
        self.client = GeminiAPIClient(api_key)
    
    def validate_inputs(self, text: str, api_key: str) -> tuple[bool, str]:
        """
        验证输入参数
        """
        if not api_key or api_key == "your_gemini_api_key_here":
            return False, "请提供有效的Gemini API密钥"
        
        if not text.strip():
            return False, "输入文本不能为空"
        
        return True, ""
    
    def process(self, text: str, enable_expansion: bool = True, 
               enable_translation: bool = True, expansion_style: str = "详细描述",
               max_tokens: int = 1000) -> tuple[str, str, str]:
        """
        处理文本
        """
        processed_text = text
        english_translation = ""
        
        try:
            # 文本扩写
            if enable_expansion:
                print("正在进行文本扩写...")
                expanded_text = self.client.expand_text(text, expansion_style, max_tokens)
                if not self._is_error_response(expanded_text):
                    processed_text = expanded_text
                else:
                    processed_text = f"扩写失败: {expanded_text}"
            
            # 英文翻译
            if enable_translation:
                print("正在进行英文翻译...")
                translation_source = processed_text if enable_expansion else text
                english_translation = self.client.translate_to_english(translation_source, max_tokens)
                if self._is_error_response(english_translation):
                    english_translation = f"翻译失败: {english_translation}"
            else:
                english_translation = "翻译功能已禁用"
            
            return text, processed_text, english_translation
            
        except Exception as e:
            error_msg = f"处理过程中发生错误: {str(e)}"
            logging.error(error_msg)
            return text, error_msg, error_msg
    
    def _is_error_response(self, response: str) -> bool:
        """
        检查响应是否为错误信息
        """
        error_keywords = ["API请求失败", "处理错误", "API调用失败", "请求超时"]
        return any(keyword in response for keyword in error_keywords)