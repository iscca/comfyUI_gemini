"""
ComfyUI Gemini文本处理器节点
"""

from .gemini_text_processor import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# 确保导出正确的映射
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# 为了兼容性，也可以直接在这里定义
WEB_DIRECTORY = "./web"