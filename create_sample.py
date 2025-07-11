#!/usr/bin/env python3
"""
Create a simple test text file that can be converted to PDF using pandoc.
"""

from pathlib import Path


def create_sample_markdown():
    """Create a sample markdown file for testing."""
    content = """# Sample Ebook

## Chapter 1: Introduction

This is the first chapter of our sample ebook. It contains some English text that can be translated to Chinese.

The purpose of this document is to demonstrate the ebook translation pipeline functionality.

## Chapter 2: Advanced Topics

This chapter covers more advanced concepts in the field of technology.

### Machine Learning

Machine learning and artificial intelligence are rapidly evolving fields that are transforming many industries.

### Data Science

Data science combines statistical analysis with programming to extract insights from large datasets.

## Chapter 3: Applications

Real-world applications of these technologies include:

- Natural language processing
- Computer vision
- Recommendation systems
- Automated decision making

## Conclusion

Thank you for reading this sample document. This concludes our brief example that demonstrates the translation pipeline capabilities.

The system should be able to process this content and generate a translated HTML output with proper formatting and table of contents.
"""
    
    filename = "sample_ebook.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Created sample markdown: {filename}")
    return filename


def convert_to_pdf(md_file):
    """Convert markdown to PDF using pandoc."""
    import subprocess
    
    pdf_file = md_file.replace('.md', '.pdf')
    
    try:
        cmd = ['pandoc', md_file, '-o', pdf_file]
        subprocess.run(cmd, check=True)
        print(f"Converted to PDF: {pdf_file}")
        return pdf_file
    except subprocess.CalledProcessError:
        print("Error: pandoc conversion failed")
        return None
    except FileNotFoundError:
        print("Error: pandoc not found. Install pandoc or use the markdown file directly.")
        return None


if __name__ == "__main__":
    # Create markdown file
    md_file = create_sample_markdown()
    
    # Try to convert to PDF
    pdf_file = convert_to_pdf(md_file)
    
    if pdf_file:
        print(f"\nSample PDF created: {pdf_file}")
        print("You can now test the pipeline with:")
        print(f"python3 main.py -i {pdf_file} --olang zh")
    else:
        print(f"\nUsing markdown file: {md_file}")
        print("You can test with the markdown file by temporarily modifying step2 to handle .md files,")
        print("or install pandoc to convert to PDF first.")
        print("\nAlternatively, find any existing PDF file and use:")
        print("python3 main.py -i your_file.pdf --olang zh")