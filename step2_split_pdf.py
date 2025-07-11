#!/usr/bin/env python3
"""
Step 2: Split PDF/Convert DOCX/EPUB
Converts input ebook to individual markdown pages.
"""

import os
import argparse
from pathlib import Path
import subprocess
import fitz  # PyMuPDF
from pdf2image import convert_from_path
import pypandoc


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


def convert_docx_epub(input_file, temp_dir):
    """Convert DOCX/EPUB to markdown using pandoc."""
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
        split_pdf(input_file, args.temp_dir)
    elif file_ext in ['.docx', '.epub']:
        if not convert_docx_epub(input_file, args.temp_dir):
            return 1
    else:
        print(f"Error: Unsupported file format {file_ext}")
        return 1
    
    print("Step 2 completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())