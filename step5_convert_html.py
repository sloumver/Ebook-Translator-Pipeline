#!/usr/bin/env python3
"""
Step 5: Convert Markdown to HTML
Converts the merged markdown file to HTML using pandoc with template.
"""

import argparse
from pathlib import Path
import subprocess
import shutil


def load_config(temp_dir):
    """Load configuration from config.txt file."""
    config_file = Path(temp_dir) / "config.txt"
    config = {}
    
    with open(config_file, 'r') as f:
        for line in f:
            key, value = line.strip().split('=', 1)
            config[key] = value
    
    return config


def check_pandoc():
    """Check if pandoc is installed and available."""
    try:
        result = subprocess.run(['pandoc', '--version'], 
                              capture_output=True, text=True, check=True)
        print("Pandoc is available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: Pandoc is not installed or not in PATH")
        print("Please install pandoc: https://pandoc.org/installing.html")
        return False


def copy_images_to_output(temp_dir, output_dir):
    """Copy images directory to output directory for HTML access."""
    images_dir = Path(temp_dir) / "images"
    output_images_dir = output_dir / "images"
    
    if images_dir.exists() and any(images_dir.iterdir()):
        if output_images_dir.exists():
            shutil.rmtree(output_images_dir)
        
        shutil.copytree(images_dir, output_images_dir)
        print(f"Copied images to {output_images_dir}")
        return True
    
    return False


def convert_to_html(temp_dir):
    """Convert merged markdown to HTML using pandoc."""
    output_dir = Path(temp_dir) / "output"
    md_file = output_dir / "output.md"
    html_file = output_dir / "output.html"
    
    if not md_file.exists():
        print(f"Error: Markdown file {md_file} does not exist.")
        print("Please run step 4 (merge markdown) first.")
        return False
    
    # Check for template
    template_file = Path("template.html")
    if not template_file.exists():
        print("Warning: template.html not found, using default pandoc template")
        template_args = []
    else:
        template_args = ["--template", str(template_file)]
    
    # Copy images to output directory
    copy_images_to_output(temp_dir, output_dir)
    
    # Build pandoc command
    pandoc_cmd = [
        "pandoc",
        str(md_file),
        "-o", str(html_file),
        "--standalone",
        "--self-contained",
        "--metadata", "title=Translated Ebook"
    ]
    
    # Add template if available
    if template_args:
        pandoc_cmd.extend(template_args)
    
    # Add CSS if available
    if Path("style.css").exists():
        pandoc_cmd.extend(["--css", "style.css"])
    
    try:
        print(f"Converting {md_file} to HTML...")
        result = subprocess.run(pandoc_cmd, capture_output=True, text=True, check=True)
        print(f"HTML file created: {html_file}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error running pandoc: {e}")
        print(f"Command: {' '.join(pandoc_cmd)}")
        print(f"Error output: {e.stderr}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Convert markdown to HTML")
    parser.add_argument("temp_dir", help="Temporary directory path")
    
    args = parser.parse_args()
    
    # Validate temp directory
    temp_path = Path(args.temp_dir)
    if not temp_path.exists():
        print(f"Error: Temporary directory {args.temp_dir} does not exist.")
        return 1
    
    # Check pandoc availability
    if not check_pandoc():
        return 1
    
    # Convert to HTML
    if not convert_to_html(args.temp_dir):
        return 1
    
    print("Step 5 completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())