#!/usr/bin/env python3
"""
Main pipeline script to run all steps sequentially.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_step(script_name, args_list, description):
    """Run a pipeline step and check for success."""
    print(f"\n{'='*60}")
    print(f"Running {description}")
    print(f"{'='*60}")
    
    cmd = [sys.executable, script_name] + args_list
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"✗ Script {script_name} not found")
        return False


def main():
    parser = argparse.ArgumentParser(description="Ebook Translation Pipeline")
    parser.add_argument("-i", "--input", required=True, help="Input ebook file path")
    parser.add_argument("-l", "--lang", help="Input text language (auto-detect if not specified)")
    parser.add_argument("--olang", default="zh", help="Output language (default: zh)")
    parser.add_argument("--api", action="store_true", help="Use Claude API for translation")
    parser.add_argument("--api-key", help="Claude API key (or set ANTHROPIC_API_KEY env var)")
    parser.add_argument("--start-step", type=int, default=1, choices=range(1, 7), 
                       help="Start from specific step (1-6)")
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file {args.input} does not exist.")
        return 1
    
    # Determine temp directory
    temp_dir = input_path.parent / f"{input_path.stem}_temp"
    
    steps = [
        ("step1_init.py", ["-i", args.input, "-l", args.lang or "", "--olang", args.olang], 
         "Step 1: Environment Initialization"),
        ("step2_split_pdf.py", [str(temp_dir)], 
         "Step 2: Split/Convert Ebook"),
        ("step3_translate.py", [str(temp_dir)] + (["--api"] if args.api else []) + 
         (["--api-key", args.api_key] if args.api_key else []), 
         "Step 3: Translate Markdown"),
        ("step4_merge_md.py", [str(temp_dir)], 
         "Step 4: Merge Markdown Files"),
        ("step5_convert_html.py", [str(temp_dir)], 
         "Step 5: Convert to HTML"),
        ("step6_generate_toc.py", [str(temp_dir)], 
         "Step 6: Generate Table of Contents")
    ]
    
    # Run steps starting from specified step
    for i, (script, script_args, description) in enumerate(steps[args.start_step-1:], args.start_step):
        # Clean up script_args - remove empty strings
        script_args = [arg for arg in script_args if arg]
        
        if not run_step(script, script_args, description):
            print(f"\nPipeline failed at step {i}")
            return 1
    
    print(f"\n{'='*60}")
    print("🎉 EBOOK TRANSLATION PIPELINE COMPLETED SUCCESSFULLY! 🎉")
    print(f"{'='*60}")
    print(f"Output files are in: {temp_dir / 'output'}")
    print(f"Final HTML file: {temp_dir / 'output' / 'output.html'}")
    
    return 0


if __name__ == "__main__":
    exit(main())