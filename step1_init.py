#!/usr/bin/env python3
"""
Step 1: Environment Initialization
Creates temporary directory and sets up the working environment.
"""

import os
import argparse
import shutil
from pathlib import Path


def create_temp_directory(input_file_path):
    """Create temporary directory based on input file name."""
    input_file = Path(input_file_path)
    temp_dir = input_file.parent / f"{input_file.stem}_temp"
    
    if temp_dir.exists():
        print(f"Warning: Temporary directory {temp_dir} already exists.")
        response = input("Do you want to remove it and create a new one? (y/n): ")
        if response.lower() == 'y':
            shutil.rmtree(temp_dir)
        else:
            print("Using existing directory.")
            return temp_dir
    
    temp_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created temporary directory: {temp_dir}")
    return temp_dir


def main():
    parser = argparse.ArgumentParser(description="Initialize environment for ebook translation")
    parser.add_argument("-i", "--input", required=True, help="Input ebook file path")
    parser.add_argument("-l", "--lang", help="Input text language (auto-detect if not specified)")
    parser.add_argument("--olang", default="zh", help="Output language (default: zh)")
    
    args = parser.parse_args()
    
    # Validate input file exists
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file {args.input} does not exist.")
        return 1
    
    # Create temporary directory
    temp_dir = create_temp_directory(args.input)
    
    # Create subdirectories
    (temp_dir / "pages").mkdir(exist_ok=True)
    (temp_dir / "images").mkdir(exist_ok=True)
    (temp_dir / "output").mkdir(exist_ok=True)
    
    # Save configuration
    config_file = temp_dir / "config.txt"
    with open(config_file, 'w') as f:
        f.write(f"INPUT_FILE={args.input}\n")
        f.write(f"INPUT_LANG={args.lang or 'auto'}\n")
        f.write(f"OUTPUT_LANG={args.olang}\n")
        f.write(f"TEMP_DIR={temp_dir}\n")
    
    print(f"Configuration saved to: {config_file}")
    print("Environment initialization completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())