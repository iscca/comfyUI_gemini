import json
import requests
import logging
from typing import Dict, Any, Tuple

class GeminiTextProcessor:
    """
    ComfyUI节点：使用Google Gemini API进行文本扩写和翻译
    """
    
    def __init__(self):
        self.type = "GeminiTextProcessor"
        self.category = "text"
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": "请输入要处理的文本"
                }),
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": "your_gemini_api_key_here"
                }),
                "enable_expansion": ("BOOLEAN", {
                    "default": True,
                    "label_on": "启用扩写",
                    "label_off": "禁用扩写"
                }),
                "enable_translation": ("BOOLEAN", {
                    "default": True,
                    "label_on": "启用翻译",
                    "label_off": "禁用翻译"
                }),
                "expansion_style": (["详细描述", "创意扩展", "专业术语", "生动形象"], {
                    "default": "详细描述"
                }),
                "max_tokens": ("INT", {
                    "default": 1000,
                    "min": 100,
                    "max": 4000,
                    "step": 100
                })
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("原始文本", "处理后文本", "英文翻译")
    FUNCTION = "process_text"
    
    def _call_gemini_api(self, api_key: str, prompt: str, max_tokens: int = 1000) -> str:
        """
        调用Google Gemini API
        """
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
            
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
                    "temperature": 0.7,
                    "topP": 0.8,
                    "topK": 40
                }
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if "candidates" in result and len(result["candidates"]) > 0:
                content = result["candidates"][0]["content"]["parts"][0]["text"]
                return content.strip()
            else:
                return "API调用失败：未返回有效内容"
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Gemini API请求错误: {e}")
            return f"API请求错误: {str(e)}"
        except KeyError as e:
            logging.error(f"API响应格式错误: {e}")
            return f"API响应格式错误: {str(e)}"
        except Exception as e:
            logging.error(f"未知错误: {e}")
            return f"处理错误: {str(e)}"
    
    def _expand_text(self, text: str, api_key: str, style: str, max_tokens: int) -> str:
        """
        扩写文本
        """
        style_prompts = {
            "详细描述": "请将以下文本进行详细扩写，增加更多描述性内容和细节：",
            "创意扩展": "请对以下文本进行创意性扩写，增加想象力和艺术性描述：",
            "专业术语": "请将以下文本扩写为更专业和技术性的描述：",
            "生动形象": "请将以下文本扩写得更加生动形象，使用比喻和修辞手法："
        }
        
        prompt = f"{style_prompts.get(style, style_prompts['详细描述'])}\n\n{text}\n\n请保持原文的核心意思，但要大幅增加内容的丰富度和表现力。"
        
        return self._call_gemini_api(api_key, prompt, max_tokens)
    
    def _translate_to_english(self, text: str, api_key: str, max_tokens: int) -> str:
        """
        翻译为英文
        """
        prompt = f"请将以下中文文本准确翻译成英文，保持原意和语境：\n\n{text}\n\n请确保翻译自然流畅，符合英文表达习惯。"
        
        return self._call_gemini_api(api_key, prompt, max_tokens)
    
    def process_text(self, text: str, api_key: str, enable_expansion: bool, 
                    enable_translation: bool, expansion_style: str, max_tokens: int) -> Tuple[str, str, str]:
        """
        处理文本的主要函数
        """
        if not api_key or api_key == "your_gemini_api_key_here":
            return (text, "错误：请提供有效的Gemini API密钥", "错误：请提供有效的Gemini API密钥")
        
        if not text.strip():
            return (text, "错误：输入文本不能为空", "错误：输入文本不能为空")
        
        processed_text = text
        english_translation = ""
        
        try:
            # 文本扩写
            if enable_expansion:
                print("正在进行文本扩写...")
                expanded_text = self._expand_text(text, api_key, expansion_style, max_tokens)
                if not expanded_text.startswith("API") and not expanded_text.startswith("处理错误"):
                    processed_text = expanded_text
                else:
                    processed_text = f"扩写失败: {expanded_text}"
            
            # 英文翻译
            if enable_translation:
                print("正在进行英文翻译...")
                translation_source = processed_text if enable_expansion else text
                english_translation = self._translate_to_english(translation_source, api_key, max_tokens)
                if english_translation.startswith("API") or english_translation.startswith("处理错误"):
                    english_translation = f"翻译失败: {english_translation}"
            else:
                english_translation = "翻译功能已禁用"
            
            return (text, processed_text, english_translation)
            
        except Exception as e:
            error_msg = f"处理过程中发生错误: {str(e)}"
            logging.error(error_msg)
            return (text, error_msg, error_msg)

# ComfyUI节点映射
NODE_CLASS_MAPPINGS = {
    "GeminiTextProcessor": GeminiTextProcessor
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GeminiTextProcessor": "Gemini文本处理器"
}