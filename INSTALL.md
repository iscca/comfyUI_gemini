# ComfyUI Gemini文本处理器 - 安装指南

## 安装方法

### 方法1：Git克隆（推荐）

1. 打开终端/命令提示符
2. 进入ComfyUI的custom_nodes目录：
   ```bash
   cd /path/to/ComfyUI/custom_nodes
   ```
3. 克隆仓库：
   ```bash
   git clone https://github.com/iscca/comfyUI_gemini.git
   ```
4. 安装依赖：
   ```bash
   cd comfyUI_gemini
   pip install -r requirements.txt
   ```

### 方法2：手动下载

1. 下载项目ZIP文件
2. 解压到ComfyUI的custom_nodes目录下
3. 确保文件夹名为 `comfyUI_gemini`
4. 安装依赖：
   ```bash
   pip install requests
   ```

## 验证安装

1. 重启ComfyUI
2. 在节点菜单中查找 "text" 分类
3. 应该能看到 "Gemini文本处理器" 节点

## 目录结构

安装后的目录结构应该如下：
```
ComfyUI/
└── custom_nodes/
    └── comfyUI_gemini/
        ├── __init__.py
        ├── gemini_text_processor.py
        ├── requirements.txt
        ├── README.md
        └── 其他文件...
```

## 故障排除

### 节点不显示
- 检查目录结构是否正确
- 确保__init__.py文件存在
- 重启ComfyUI

### 导入错误
- 确保安装了requests库：`pip install requests`
- 检查Python环境是否正确

### API调用失败
- 确保提供了有效的Gemini API密钥
- 检查网络连接
- 确认API配额充足

## 获取API密钥

1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 登录Google账号
3. 创建新的API密钥
4. 复制密钥用于节点配置

## 使用示例

1. 添加"Gemini文本处理器"节点到工作流
2. 输入要处理的文本
3. 填入Gemini API密钥
4. 选择扩写风格
5. 启用/禁用扩写和翻译功能
6. 运行工作流查看结果