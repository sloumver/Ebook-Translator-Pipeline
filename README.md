# Ebook Translator Pipeline

一套自动化的电子书翻译工具链，支持 PDF/DOCX/EPUB/Markdown 格式的电子书，使用 SiliconFlow AI API 进行翻译，输出带目录的中文 HTML 文件。

## 功能特性

- 支持多种格式：PDF、DOCX、EPUB、Markdown
- 分步骤处理，可从任意步骤重新开始
- 使用 SiliconFlow AI API 自动翻译或手动翻译
- 自动生成目录 (TOC)
- 图片资源保留
- 响应式 HTML 输出

## 安装依赖

```bash
# 核心依赖（必需）
pip install requests

# 可选依赖（根据需要安装）
pip install -r requirements.txt
```

系统依赖（可选）：
- `pandoc`: https://pandoc.org/installing.html（用于DOCX/EPUB转换）
- `poppler-utils` (Linux/Mac) 或 `poppler` (Windows)（用于PDF处理）

## 配置API密钥

### SiliconFlow API

1. 注册SiliconFlow账号：https://siliconflow.cn
2. 获取API密钥
3. 设置环境变量：

```bash
export SILICONFLOW_API_KEY="your-api-key"
```

或在命令行中直接指定：
```bash
python3 main.py -i your-file.pdf --api --api-key "your-api-key"
```

## 使用方法

### 完整流程

```bash
# 创建示例文件（可选）
python3 create_sample.py

# 使用SiliconFlow API翻译
python3 main.py -i sample_ebook.md --api --olang zh

# 手动翻译模式
python3 main.py -i sample_ebook.md --olang zh
```

### 从指定步骤开始

```bash
python3 main.py -i sample_ebook.md --start-step 3 --api
```

### 命令行参数

- `-i, --input`: 输入电子书路径（必填）
- `-l, --lang`: 输入文本语言（可选，默认自动识别）
- `--olang`: 输出语言（默认 zh）
- `--api`: 使用SiliconFlow API翻译
- `--api-key`: SiliconFlow API密钥
- `--start-step`: 从指定步骤开始（1-6）

## 处理步骤

1. **步骤 1**: 环境初始化 (`step1_init.py`)
2. **步骤 2**: 拆分/转换电子书 (`step2_split_pdf.py`)
3. **步骤 3**: 翻译 Markdown (`step3_translate.py`)
4. **步骤 4**: 合并 Markdown (`step4_merge_md.py`)
5. **步骤 5**: 转换为 HTML (`step5_convert_html.py`)
6. **步骤 6**: 生成目录 (`step6_generate_toc.py`)

## 输出结构

```
inputbook_temp/
├── config.txt          # 配置文件
├── pages/              # 原始页面 markdown
├── images/             # 提取的图片
└── output/             # 输出文件
    ├── output_page*.md # 翻译后的页面
    ├── output.md       # 合并的 markdown
    └── output.html     # 最终 HTML 文件
```

## SiliconFlow API 特性

- **高质量翻译**: 使用Qwen2.5-7B-Instruct模型
- **格式保持**: 自动保持Markdown格式和结构
- **成本效益**: 相比其他API更经济实惠
- **支持多语言**: 支持中英日韩法德西俄等多种语言

## 翻译质量优化

- 使用专门的翻译提示词确保质量
- 保持原文格式和Markdown语法
- 支持批量翻译，自动跳过已翻译文件
- 错误处理和重试机制

## 手动翻译模式

如果不使用API或API失败，程序会自动切换到手动翻译模式，提示您逐页翻译内容。

## 故障排除

1. **API错误**: 检查API密钥是否正确，网络连接是否正常
2. **依赖错误**: 确保安装了必要的依赖包
3. **文件格式**: 确保输入文件格式受支持
4. **权限问题**: 确保对工作目录有写权限

## 示例

```bash
# 完整示例：英文PDF翻译为中文
python3 main.py -i document.pdf --api --olang zh

# 手动翻译模式
python3 main.py -i document.md --olang zh

# 从翻译步骤开始（跳过文档拆分）
python3 main.py -i document.pdf --start-step 3 --api
```

## 许可证

MIT License