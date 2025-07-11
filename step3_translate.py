#!/usr/bin/env python3
"""
Step 3: Translate Markdown Files
Translates individual markdown pages using Claude API or manual translation.
"""

import os
import argparse
from pathlib import Path
import glob
from typing import Optional

# Try to import optional dependencies
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


def load_config(temp_dir):
    """Load configuration from config.txt file."""
    config_file = Path(temp_dir) / "config.txt"
    config = {}
    
    with open(config_file, 'r') as f:
        for line in f:
            key, value = line.strip().split('=', 1)
            config[key] = value
    
    return config


def translate_with_claude(content: str, target_lang: str, api_key: Optional[str] = None) -> str:
    """Translate content using Claude API."""
    if not ANTHROPIC_AVAILABLE:
        raise ValueError("anthropic library not installed. Install with: pip install anthropic")
    
    if not api_key:
        # Try to get from environment
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    client = anthropic.Anthropic(api_key=api_key)
    
    prompt = f"""Please translate the following markdown content to {target_lang}. 
Preserve all markdown formatting, including headers, links, and image references.
Only translate the text content, keep all markdown syntax unchanged.

Content to translate:
{content}

Translated content:"""
    
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=4000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text


def manual_translation_prompt(md_file, target_lang):
    """Generate manual translation prompt for user."""
    print(f"\n{'='*60}")
    print(f"MANUAL TRANSLATION REQUIRED")
    print(f"{'='*60}")
    print(f"File: {md_file}")
    print(f"Target Language: {target_lang}")
    print(f"{'='*60}")
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Original content:")
    print(content)
    print(f"{'='*60}")
    print(f"Please translate the above content to {target_lang}")
    print("Preserve all markdown formatting.")
    print("Enter the translated content (press Ctrl+D when finished):")
    
    translated_lines = []
    try:
        while True:
            line = input()
            translated_lines.append(line)
    except EOFError:
        pass
    
    return '\n'.join(translated_lines)


def translate_markdown_files(temp_dir, use_api=False, api_key=None):
    """Translate all markdown files in the pages directory."""
    config = load_config(temp_dir)
    target_lang = config['OUTPUT_LANG']
    
    pages_dir = Path(temp_dir) / "pages"
    output_dir = Path(temp_dir) / "output"
    
    # Get all page markdown files
    md_files = sorted(glob.glob(str(pages_dir / "page*.md")))
    
    if not md_files:
        print("No markdown files found to translate.")
        return False
    
    print(f"Found {len(md_files)} files to translate to {target_lang}")
    
    for md_file in md_files:
        md_path = Path(md_file)
        output_filename = f"output_{md_path.name}"
        output_path = output_dir / output_filename
        
        # Skip if already translated
        if output_path.exists():
            print(f"Skipping {md_path.name} - already translated")
            continue
        
        print(f"Translating {md_path.name}...")
        
        # Read original content
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            if use_api:
                # Use Claude API
                translated_content = translate_with_claude(content, target_lang, api_key)
            else:
                # Manual translation
                translated_content = manual_translation_prompt(md_file, target_lang)
            
            # Save translated content
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            
            print(f"Translated: {output_filename}")
            
        except Exception as e:
            print(f"Error translating {md_path.name}: {e}")
            continue
    
    print("Translation completed!")
    return True


def main():
    parser = argparse.ArgumentParser(description="Translate markdown pages")
    parser.add_argument("temp_dir", help="Temporary directory path")
    parser.add_argument("--api", action="store_true", help="Use Claude API for translation")
    parser.add_argument("--api-key", help="Claude API key (or set ANTHROPIC_API_KEY env var)")
    
    args = parser.parse_args()
    
    # Validate temp directory
    temp_path = Path(args.temp_dir)
    if not temp_path.exists():
        print(f"Error: Temporary directory {args.temp_dir} does not exist.")
        return 1
    
    # Perform translation
    if not translate_markdown_files(args.temp_dir, args.api, args.api_key):
        return 1
    
    print("Step 3 completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main())