#!/usr/bin/env python3
"""
Step 2: Split PDF/Convert DOCX/EPUB
Converts input ebook to individual markdown pages.
"""

import os
import argparse
from pathlib import Path
import subprocess

# Try to import optional dependencies
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False

try:
    import pypandoc
    PYPANDOC_AVAILABLE = True
except ImportError:
    PYPANDOC_AVAILABLE = False


def load_config(temp_dir):
    """Load configuration from config.txt file."""
    config_file = Path(temp_dir) / "config.txt"
    config = {}
    
    with open(config_file, 'r') as f:
        for line in f:
            key, value = line.strip().split('=', 1)
            config[key] = value
    
    return config


def split_pdf(input_file, temp_dir):
    """Split PDF into individual markdown pages."""
    if not PYMUPDF_AVAILABLE:
        print("Error: PyMuPDF (fitz) not installed. Install with: pip install PyMuPDF")
        return False
    
    pdf_document = fitz.open(input_file)
    pages_dir = Path(temp_dir) / "pages"
    images_dir = Path(temp_dir) / "images"
    
    total_pages = len(pdf_document)
    print(f"Processing {total_pages} pages from PDF...")
    
    for page_num in range(total_pages):
        page = pdf_document.load_page(page_num)
        
        # Extract text
        text = page.get_text()
        
        # Extract images
        image_list = page.get_images()
        page_images = []
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            pix = fitz.Pixmap(pdf_document, xref)
            
            if pix.n - pix.alpha < 4:  # GRAY or RGB
                img_filename = f"page{page_num+1:04d}_img{img_index+1:03d}.png"
                img_path = images_dir / img_filename
                pix.save(str(img_path))
                page_images.append(f"![Image {img_index+1}](../images/{img_filename})")
            
            pix = None
        
        # Create markdown content
        md_content = f"# Page {page_num+1}\n\n"
        md_content += text + "\n\n"
        
        if page_images:
            md_content += "## Images\n\n"
            md_content += "\n\n".join(page_images) + "\n\n"
        
        # Save markdown file
        md_filename = f"page{page_num+1:04d}.md"
        md_path = pages_dir / md_filename
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"Created: {md_filename}")
    
    pdf_document.close()
    print(f"PDF splitting completed. Created {total_pages} markdown files.")
    return True


def handle_markdown_file(input_file, temp_dir):
    """Handle markdown files directly by splitting on headers."""
    pages_dir = Path(temp_dir) / "pages"
    input_path = Path(input_file)
    
    try:
        # Read the markdown file
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by main headers (# )
        sections = content.split('\n# ')
        
        for i, section_content in enumerate(sections):
            if i == 0:
                # First section doesn't need '# ' prefix added back
                md_content = section_content
            else:
                md_content = '# ' + section_content
            
            # Skip empty sections
            if not md_content.strip():
                continue
            
            md_filename = f"page{i+1:04d}.md"
            md_path = pages_dir / md_filename
            
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            print(f"Created: {md_filename}")
        
        print(f"Markdown splitting completed. Created {len([s for s in sections if s.strip()])} pages.")
        return True
        
    except Exception as e:
        print(f"Error processing markdown file: {e}")
        return False


def convert_docx_epub(input_file, temp_dir):
    """Convert DOCX/EPUB to markdown using pandoc."""
    if not PYPANDOC_AVAILABLE:
        print("Error: pypandoc not installed. Install with: pip install pypandoc")
        return False
    
    pages_dir = Path(temp_dir) / "pages"
    input_path = Path(input_file)
    
    # Convert to single markdown file first
    temp_md = pages_dir / "temp_full.md"
    
    try:
        output = pypandoc.convert_file(str(input_path), 'md', outputfile=str(temp_md))
        print(f"Converted {input_path.suffix} to markdown")
        
        # Read the converted markdown
        with open(temp_md, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by headings or page breaks (simple implementation)
        pages = content.split('\n# ')
        
        for i, page_content in enumerate(pages):
            if i == 0:
                # First page doesn't need '# ' prefix added back
                md_content = page_content
            else:
                md_content = '# ' + page_content
            
            md_filename = f"page{i+1:04d}.md"
            md_path = pages_dir / md_filename
            
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            print(f"Created: {md_filename}")
        
        # Remove temporary file
        temp_md.unlink()
        
        print(f"Document splitting completed. Created {len(pages)} markdown files.")
        
    except Exception as e:
        print(f"Error converting {input_path.suffix} file: {e}")
        return False
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Split ebook into markdown pages")
    parser.add_argument("temp_dir", help="Temporary directory path")
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.temp_dir)
    input_file = config['INPUT_FILE']
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"Error: Input file {input_file} does not exist.")
        return 1
    
    # Process based on file extension
    file_ext = input_path.suffix.lower()
    
    if file_ext == '.pdf':
        if not split_pdf(input_file, args.temp_dir):
            return 1
    elif file_ext in ['.docx', '.epub']:
        if not convert_docx_epub(input_file, args.temp_dir):
            return 1
    elif file_ext == '.md':
        # Handle markdown files directly
        if not handle_markdown_file(input_file, args.temp_dir):
            return 1
    else:
        print(f"Error: Unsupported file format {file_ext}")
        return 1
    
    print("Step 2 completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())