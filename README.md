# Ebook Translator Pipeline

一套自动化的电子书翻译工具链，支持 PDF/DOCX/EPUB 格式的电子书，输出翻译后的中文 HTML 文件。

## 功能特性

- 支持多种格式：PDF、DOCX、EPUB
- 分步骤处理，可从任意步骤重新开始
- 支持 Claude API 自动翻译或手动翻译
- 自动生成目录 (TOC)
- 图片资源保留
- 响应式 HTML 输出

## 安装依赖

```bash
pip install -r requirements.txt
```

系统依赖（需要单独安装）：
- `pandoc`: https://pandoc.org/installing.html
- `poppler-utils` (Linux/Mac) 或 `poppler` (Windows)

## 使用方法

### 完整流程

```bash
python main.py -i inputbook.pdf --olang zh
```

### 使用 Claude API 翻译

```bash
export ANTHROPIC_API_KEY="your-api-key"
python main.py -i inputbook.pdf --api --olang zh
```

### 从指定步骤开始

```bash
python main.py -i inputbook.pdf --start-step 3
```

### 命令行参数

- `-i, --input`: 输入电子书路径（必填）
- `-l, --lang`: 输入文本语言（可选，默认自动识别）
- `--olang`: 输出语言（默认 zh）
- `--api`: 使用 Claude API 翻译
- `--api-key`: Claude API 密钥
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

## 手动翻译

如果不使用 Claude API，程序会提示您手动翻译每一页的内容。按照提示复制、翻译、粘贴即可。

## 注意事项

- 确保安装了所有系统依赖（pandoc, poppler-utils）
- PDF 文件将按页拆分，大文件可能需要较长处理时间
- 使用 Claude API 需要有效的 API 密钥
- 输出的 HTML 文件包含响应式设计，适合各种设备查看