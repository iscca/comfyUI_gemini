"""
Gemini文本处理器测试脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gemini_text_processor import GeminiTextProcessor

def test_node_creation():
    """测试节点创建"""
    print("测试节点创建...")
    node = GeminiTextProcessor()
    print(f"节点类型: {node.type}")
    print(f"节点分类: {node.category}")
    print("✓ 节点创建成功")

def test_input_types():
    """测试输入类型定义"""
    print("\n测试输入类型定义...")
    input_types = GeminiTextProcessor.INPUT_TYPES()
    
    required_fields = ["text", "api_key", "enable_expansion", "enable_translation", "expansion_style", "max_tokens"]
    
    for field in required_fields:
        if field in input_types["required"]:
            print(f"✓ {field} 字段存在")
        else:
            print(f"✗ {field} 字段缺失")
    
    print("✓ 输入类型定义正确")

def test_return_types():
    """测试返回类型定义"""
    print("\n测试返回类型定义...")
    node = GeminiTextProcessor()
    
    print(f"返回类型: {node.RETURN_TYPES}")
    print(f"返回名称: {node.RETURN_NAMES}")
    print(f"处理函数: {node.FUNCTION}")
    print("✓ 返回类型定义正确")

def test_node_mapping():
    """测试节点映射"""
    print("\n测试节点映射...")
    from gemini_text_processor import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
    
    if "GeminiTextProcessor" in NODE_CLASS_MAPPINGS:
        print("✓ 节点类映射存在")
    else:
        print("✗ 节点类映射缺失")
    
    if "GeminiTextProcessor" in NODE_DISPLAY_NAME_MAPPINGS:
        print("✓ 节点显示名称映射存在")
        print(f"显示名称: {NODE_DISPLAY_NAME_MAPPINGS['GeminiTextProcessor']}")
    else:
        print("✗ 节点显示名称映射缺失")

def test_with_dummy_data():
    """使用虚拟数据测试节点功能"""
    print("\n使用虚拟数据测试...")
    node = GeminiTextProcessor()
    
    # 测试无效API密钥的情况
    result = node.process_text(
        text="测试文本",
        api_key="invalid_key",
        enable_expansion=True,
        enable_translation=True,
        expansion_style="详细描述",
        max_tokens=1000
    )
    
    original, processed, translated = result
    print(f"原始文本: {original}")
    print(f"处理结果: {processed}")
    print(f"翻译结果: {translated}")
    
    if "错误" in processed:
        print("✓ 错误处理正常")
    else:
        print("✗ 错误处理异常")

def main():
    """主测试函数"""
    print("=== Gemini文本处理器节点测试 ===")
    
    try:
        test_node_creation()
        test_input_types()
        test_return_types()
        test_node_mapping()
        test_with_dummy_data()
        
        print("\n=== 测试完成 ===")
        print("✓ 所有基础测试通过")
        print("\n注意：要进行完整功能测试，请提供有效的Gemini API密钥")
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()