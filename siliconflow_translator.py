#!/usr/bin/env python3
"""
SiliconFlow AI Translation Module
使用SiliconFlow API进行文本翻译
"""

import requests
import json
import os
from typing import Optional


class SiliconFlowTranslator:
    """SiliconFlow翻译服务类"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化翻译器
        
        Args:
            api_key: SiliconFlow API密钥，如果未提供则从环境变量获取
        """
        self.api_key = api_key or os.environ.get('SILICONFLOW_API_KEY')
        if not self.api_key:
            raise ValueError("SiliconFlow API key is required. Set SILICONFLOW_API_KEY environment variable or pass api_key parameter.")
        
        self.base_url = "https://api.siliconflow.cn/v1/chat/completions"
        self.model = "Qwen/Qwen2.5-7B-Instruct"  # 使用更适合翻译的模型
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def translate_text(self, text: str, target_language: str = "zh", source_language: str = "auto") -> str:
        """
        翻译文本
        
        Args:
            text: 要翻译的文本
            target_language: 目标语言（zh=中文, en=英文等）
            source_language: 源语言（auto=自动检测）
        
        Returns:
            翻译后的文本
        """
        # 构建翻译提示词
        language_map = {
            "zh": "中文",
            "en": "English", 
            "ja": "日语",
            "ko": "韩语",
            "fr": "法语",
            "de": "德语",
            "es": "西班牙语",
            "ru": "俄语"
        }
        
        target_lang_name = language_map.get(target_language, target_language)
        
        if source_language == "auto":
            prompt = f"""请将以下文本翻译成{target_lang_name}。保持原文的格式和结构，包括markdown语法、换行符等。只返回翻译结果，不要添加任何解释或说明。

原文:
{text}

翻译:"""
        else:
            source_lang_name = language_map.get(source_language, source_language)
            prompt = f"""请将以下{source_lang_name}文本翻译成{target_lang_name}。保持原文的格式和结构，包括markdown语法、换行符等。只返回翻译结果，不要添加任何解释或说明。

原文:
{text}

翻译:"""
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,  # 较低的温度以确保翻译一致性
            "max_tokens": 4000
        }
        
        try:
            response = requests.post(self.base_url, json=payload, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            translated_text = result['choices'][0]['message']['content'].strip()
            
            return translated_text
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"SiliconFlow API request failed: {e}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Unexpected response format from SiliconFlow API: {e}")
    
    def translate_markdown(self, markdown_content: str, target_language: str = "zh") -> str:
        """
        翻译Markdown内容，保持格式
        
        Args:
            markdown_content: Markdown格式的内容
            target_language: 目标语言
        
        Returns:
            翻译后的Markdown内容
        """
        return self.translate_text(markdown_content, target_language)


def test_translation():
    """测试翻译功能"""
    try:
        translator = SiliconFlowTranslator()
        
        # 测试简单文本翻译
        test_text = "Hello, this is a test for translation."
        result = translator.translate_text(test_text, "zh")
        print(f"Original: {test_text}")
        print(f"Translated: {result}")
        
        # 测试Markdown翻译
        test_markdown = """# Hello World

This is a **sample** markdown text with [links](http://example.com) and lists:

- Item 1
- Item 2
- Item 3

## Conclusion

Thank you for reading!"""
        
        result_md = translator.translate_markdown(test_markdown, "zh")
        print(f"\nMarkdown Original:\n{test_markdown}")
        print(f"\nMarkdown Translated:\n{result_md}")
        
    except Exception as e:
        print(f"Test failed: {e}")


if __name__ == "__main__":
    test_translation()