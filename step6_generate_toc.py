#!/usr/bin/env python3
"""
Step 6: Generate Table of Contents (TOC)
Generates and inserts TOC at the beginning of the HTML file.
"""

import argparse
from pathlib import Path
import re

# Try to import optional dependencies
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False


def load_config(temp_dir):
    """Load configuration from config.txt file."""
    config_file = Path(temp_dir) / "config.txt"
    config = {}
    
    with open(config_file, 'r') as f:
        for line in f:
            key, value = line.strip().split('=', 1)
            config[key] = value
    
    return config


def generate_toc_simple(html_content):
    """Generate TOC using simple regex parsing (fallback when BeautifulSoup not available)."""
    import re
    
    # Find all heading tags
    heading_pattern = r'<(h[1-6])[^>]*id="([^"]*)"[^>]*>([^<]+)</h[1-6]>'
    headings = re.findall(heading_pattern, html_content, re.IGNORECASE)
    
    if not headings:
        # Try to find headings without id and add them
        heading_pattern_no_id = r'<(h[1-6])[^>]*>([^<]+)</h[1-6]>'
        headings_no_id = re.findall(heading_pattern_no_id, html_content, re.IGNORECASE)
        
        if not headings_no_id:
            print("No headings found in HTML file.")
            return html_content
        
        # Add IDs to headings without them
        for i, (tag, text) in enumerate(headings_no_id):
            heading_id = f"heading-{i+1}-{re.sub(r'[^w]', '-', text.lower())}"
            old_heading = f'<{tag}>{text}</{tag}>'
            new_heading = f'<{tag} id="{heading_id}">{text}</{tag}>'
            html_content = html_content.replace(old_heading, new_heading, 1)
            headings.append((tag, heading_id, text))
    
    if not headings:
        return html_content
    
    print(f"Found {len(headings)} headings for TOC")
    
    # Generate TOC HTML
    toc_html = '''
<div id="table-of-contents">
<h2>Table of Contents</h2>
<ul>
'''
    
    for tag, anchor_id, text in headings:
        level = int(tag[1])  # h1 -> 1, h2 -> 2, etc.
        indent = '  ' * (level - 1)
        toc_html += f'{indent}<li><a href="#{anchor_id}">{text}</a></li>\n'
    
    toc_html += '''</ul>
</div>

'''
    
    # Add TOC styles
    toc_styles = '''
<style>
#table-of-contents {
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 20px;
    margin: 20px 0;
}

#table-of-contents h2 {
    margin-top: 0;
    color: #333;
    border-bottom: 2px solid #007acc;
    padding-bottom: 5px;
}

#table-of-contents ul {
    list-style-type: none;
    padding-left: 0;
}

#table-of-contents li {
    margin: 5px 0;
    padding-left: 20px;
}

#table-of-contents a {
    text-decoration: none;
    color: #007acc;
}

#table-of-contents a:hover {
    text-decoration: underline;
    color: #005fa3;
}
</style>
'''
    
    # Insert styles in head
    if '<head>' in html_content:
        html_content = html_content.replace('<head>', f'<head>\n{toc_styles}', 1)
    else:
        # Add styles at the beginning
        html_content = toc_styles + html_content
    
    # Insert TOC after opening body tag
    if '<body>' in html_content:
        html_content = html_content.replace('<body>', f'<body>\n{toc_html}', 1)
    else:
        # Add TOC at the beginning
        html_content = toc_html + html_content
    
    return html_content


def generate_toc_from_headings(soup):
    """Generate TOC from heading tags (h1, h2, h3, etc.)."""
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    if not headings:
        print("No headings found in HTML file.")
        return None
    
    print(f"Found {len(headings)} headings for TOC")
    
    toc_html = '<div id="table-of-contents">\n<h2>Table of Contents</h2>\n<ul>\n'
    
    for i, heading in enumerate(headings):
        # Generate anchor ID if not present
        if not heading.get('id'):
            # Create ID from heading text
            heading_text = heading.get_text().strip()
            anchor_id = re.sub(r'[^\w\s-]', '', heading_text.lower())
            anchor_id = re.sub(r'[-\s]+', '-', anchor_id)
            anchor_id = f"heading-{i+1}-{anchor_id}"
            heading['id'] = anchor_id
        else:
            anchor_id = heading['id']
        
        # Get heading level for indentation
        level = int(heading.name[1])  # h1 -> 1, h2 -> 2, etc.
        indent = '  ' * (level - 1)
        
        heading_text = heading.get_text().strip()
        
        toc_html += f'{indent}<li><a href="#{anchor_id}">{heading_text}</a></li>\n'
    
    toc_html += '</ul>\n</div>\n'
    
    return toc_html


def add_toc_styles():
    """Generate CSS styles for TOC."""
    return """
<style>
#table-of-contents {
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 20px;
    margin: 20px 0;
}

#table-of-contents h2 {
    margin-top: 0;
    color: #333;
    border-bottom: 2px solid #007acc;
    padding-bottom: 5px;
}

#table-of-contents ul {
    list-style-type: none;
    padding-left: 0;
}

#table-of-contents li {
    margin: 5px 0;
    padding-left: 20px;
}

#table-of-contents a {
    text-decoration: none;
    color: #007acc;
}

#table-of-contents a:hover {
    text-decoration: underline;
    color: #005fa3;
}
</style>
"""


def generate_toc(temp_dir):
    """Generate and insert TOC into HTML file."""
    output_dir = Path(temp_dir) / "output"
    html_file = output_dir / "output.html"
    
    if not html_file.exists():
        print(f"Error: HTML file {html_file} does not exist.")
        print("Please run step 5 (convert to HTML) first.")
        return False
    
    # Read HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    if BS4_AVAILABLE:
        # Use BeautifulSoup if available
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Generate TOC
        toc_html = generate_toc_from_headings(soup)
        
        if not toc_html:
            print("No TOC generated - no headings found.")
            return True
        
        # Add TOC styles to head
        head = soup.find('head')
        if head:
            style_tag = BeautifulSoup(add_toc_styles(), 'html.parser')
            head.append(style_tag)
        
        # Find body and insert TOC at the beginning
        body = soup.find('body')
        if body:
            # Create TOC element
            toc_soup = BeautifulSoup(toc_html, 'html.parser')
            
            # Insert TOC as first element in body
            if body.contents:
                body.insert(0, toc_soup)
            else:
                body.append(toc_soup)
        else:
            print("Warning: No body tag found, appending TOC to end of HTML")
            soup.append(BeautifulSoup(toc_html, 'html.parser'))
        
        # Write updated HTML
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"TOC generated and inserted into {html_file}")
    else:
        # Use simple regex-based approach
        print("BeautifulSoup not available, using simple TOC generation...")
        updated_html = generate_toc_simple(html_content)
        
        # Write updated HTML
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        print(f"TOC generated and inserted into {html_file}")
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate Table of Contents for HTML")
    parser.add_argument("temp_dir", help="Temporary directory path")
    
    args = parser.parse_args()
    
    # Validate temp directory
    temp_path = Path(args.temp_dir)
    if not temp_path.exists():
        print(f"Error: Temporary directory {args.temp_dir} does not exist.")
        return 1
    
    # Generate TOC
    if not generate_toc(args.temp_dir):
        return 1
    
    print("Step 6 completed successfully!")
    print("Ebook translation pipeline completed!")
    return 0


if __name__ == "__main__":
    exit(main())