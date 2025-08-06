"""
Gemini文本处理器配置文件
"""

# 默认配置
DEFAULT_CONFIG = {
    "api_base_url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
    "timeout": 30,
    "max_retries": 3,
    "default_temperature": 0.7,
    "default_top_p": 0.8,
    "default_top_k": 40
}

# 扩写风格配置
EXPANSION_STYLES = {
    "详细描述": {
        "prompt_prefix": "请将以下文本进行详细扩写，增加更多描述性内容和细节：",
        "temperature": 0.7
    },
    "创意扩展": {
        "prompt_prefix": "请对以下文本进行创意性扩写，增加想象力和艺术性描述：",
        "temperature": 0.9
    },
    "专业术语": {
        "prompt_prefix": "请将以下文本扩写为更专业和技术性的描述：",
        "temperature": 0.5
    },
    "生动形象": {
        "prompt_prefix": "请将以下文本扩写得更加生动形象，使用比喻和修辞手法：",
        "temperature": 0.8
    }
}

# 翻译配置
TRANSLATION_CONFIG = {
    "prompt_template": "请将以下中文文本准确翻译成英文，保持原意和语境：\n\n{text}\n\n请确保翻译自然流畅，符合英文表达习惯。",
    "temperature": 0.3
}