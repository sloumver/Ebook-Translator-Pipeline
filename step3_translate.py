#!/usr/bin/env python3
"""
Step 3: Translate Markdown Files
使用SiliconFlow API翻译markdown文件
"""

import os
import argparse
from pathlib import Path
import glob
from typing import Optional
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from siliconflow_translator import SiliconFlowTranslator


def load_config(temp_dir):
    """从config.txt文件加载配置"""
    config_file = Path(temp_dir) / "config.txt"
    config = {}
    
    with open(config_file, 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                config[key] = value
    
    return config


def manual_translation_prompt(md_file, target_lang):
    """生成手动翻译提示"""
    print(f"\n{'='*60}")
    print(f"手动翻译模式")
    print(f"{'='*60}")
    print(f"文件: {md_file}")
    print(f"目标语言: {target_lang}")
    print(f"{'='*60}")
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("原文内容:")
    print(content)
    print(f"{'='*60}")
    print(f"请将上述内容翻译为{target_lang}")
    print("保持所有markdown格式不变")
    print("输入翻译内容 (完成后按Ctrl+D):")
    
    translated_lines = []
    try:
        while True:
            line = input()
            translated_lines.append(line)
    except EOFError:
        pass
    
    return '\n'.join(translated_lines)


def translate_markdown_files(temp_dir, use_api=False, api_key=None):
    """翻译所有markdown文件"""
    config = load_config(temp_dir)
    target_lang = config['OUTPUT_LANG']
    
    pages_dir = Path(temp_dir) / "pages"
    output_dir = Path(temp_dir) / "output"
    
    # 获取所有页面markdown文件
    md_files = sorted(glob.glob(str(pages_dir / "page*.md")))
    
    if not md_files:
        print("未找到需要翻译的markdown文件")
        return False
    
    print(f"找到 {len(md_files)} 个文件需要翻译为 {target_lang}")
    
    # 初始化翻译器（如果使用API）
    translator = None
    if use_api:
        try:
            translator = SiliconFlowTranslator(api_key)
            print("SiliconFlow API翻译器初始化成功")
        except Exception as e:
            print(f"SiliconFlow API初始化失败: {e}")
            print("切换到手动翻译模式")
            use_api = False
    
    for md_file in md_files:
        md_path = Path(md_file)
        output_filename = f"output_{md_path.name}"
        output_path = output_dir / output_filename
        
        # 跳过已翻译的文件
        if output_path.exists():
            print(f"跳过 {md_path.name} - 已翻译")
            continue
        
        print(f"正在翻译 {md_path.name}...")
        
        # 读取原文内容
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            if use_api and translator:
                # 使用SiliconFlow API翻译
                print("使用SiliconFlow API翻译中...")
                translated_content = translator.translate_markdown(content, target_lang)
            else:
                # 手动翻译
                translated_content = manual_translation_prompt(md_file, target_lang)
            
            # 保存翻译内容
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            
            print(f"翻译完成: {output_filename}")
            
        except Exception as e:
            print(f"翻译 {md_path.name} 时出错: {e}")
            continue
    
    print("翻译完成!")
    return True


def main():
    parser = argparse.ArgumentParser(description="翻译markdown页面")
    parser.add_argument("temp_dir", help="临时目录路径")
    parser.add_argument("--api", action="store_true", help="使用SiliconFlow API翻译")
    parser.add_argument("--api-key", help="SiliconFlow API密钥 (或设置SILICONFLOW_API_KEY环境变量)")
    
    args = parser.parse_args()
    
    # 验证临时目录
    temp_path = Path(args.temp_dir)
    if not temp_path.exists():
        print(f"错误: 临时目录 {args.temp_dir} 不存在")
        return 1
    
    # 执行翻译
    if not translate_markdown_files(args.temp_dir, args.api, args.api_key):
        return 1
    
    print("步骤3完成!")
    return 0


if __name__ == "__main__":
    exit(main())