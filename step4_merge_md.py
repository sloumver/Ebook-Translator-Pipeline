#!/usr/bin/env python3
"""
Step 4: Merge Markdown Files
Merges all translated markdown files into a single output.md file.
"""

import argparse
from pathlib import Path
import glob
import re


def load_config(temp_dir):
    """Load configuration from config.txt file."""
    config_file = Path(temp_dir) / "config.txt"
    config = {}
    
    with open(config_file, 'r') as f:
        for line in f:
            key, value = line.strip().split('=', 1)
            config[key] = value
    
    return config


def natural_sort_key(text):
    """Generate a key for natural sorting of filenames."""
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', text)]


def merge_markdown_files(temp_dir):
    """Merge all translated markdown files into output.md."""
    output_dir = Path(temp_dir) / "output"
    
    # Get all translated markdown files
    translated_files = glob.glob(str(output_dir / "output_page*.md"))
    
    if not translated_files:
        print("No translated markdown files found.")
        return False
    
    # Sort files naturally (page0001, page0002, etc.)
    translated_files.sort(key=natural_sort_key)
    
    print(f"Found {len(translated_files)} translated files to merge")
    
    # Output file
    output_file = output_dir / "output.md"
    
    with open(output_file, 'w', encoding='utf-8') as outf:
        for i, md_file in enumerate(translated_files):
            print(f"Merging {Path(md_file).name}")
            
            # Read content
            with open(md_file, 'r', encoding='utf-8') as inf:
                content = inf.read().strip()
            
            # Write content
            outf.write(content)
            
            # Add page separator (except for the last page)
            if i < len(translated_files) - 1:
                outf.write('\n\n---\n\n')
    
    print(f"Merged {len(translated_files)} files into {output_file}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Merge translated markdown files")
    parser.add_argument("temp_dir", help="Temporary directory path")
    
    args = parser.parse_args()
    
    # Validate temp directory
    temp_path = Path(args.temp_dir)
    if not temp_path.exists():
        print(f"Error: Temporary directory {args.temp_dir} does not exist.")
        return 1
    
    # Merge files
    if not merge_markdown_files(args.temp_dir):
        return 1
    
    print("Step 4 completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())