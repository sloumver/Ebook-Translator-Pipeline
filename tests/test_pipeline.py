#!/usr/bin/env python3
"""
Unit tests for the Ebook Translator Pipeline
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import os
import sys

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from step1_init import create_temp_directory
from step4_merge_md import natural_sort_key


class TestStep1Init(unittest.TestCase):
    """Test environment initialization functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test.pdf"
        self.test_file.touch()
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    def test_create_temp_directory(self):
        """Test temp directory creation."""
        temp_dir = create_temp_directory(str(self.test_file))
        
        self.assertTrue(temp_dir.exists())
        self.assertTrue(temp_dir.is_dir())
        self.assertEqual(temp_dir.name, "test_temp")
        
        # Clean up
        shutil.rmtree(temp_dir)


class TestStep4MergeMd(unittest.TestCase):
    """Test markdown merging functions."""
    
    def test_natural_sort_key(self):
        """Test natural sorting of filenames."""
        filenames = [
            "page10.md",
            "page2.md", 
            "page1.md",
            "page20.md"
        ]
        
        sorted_names = sorted(filenames, key=natural_sort_key)
        expected = ["page1.md", "page2.md", "page10.md", "page20.md"]
        
        self.assertEqual(sorted_names, expected)


class TestProjectStructure(unittest.TestCase):
    """Test project structure and file existence."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.project_root = Path(__file__).parent.parent
    
    def test_required_files_exist(self):
        """Test that all required files exist."""
        required_files = [
            "main.py",
            "step1_init.py",
            "step2_split_pdf.py", 
            "step3_translate.py",
            "step4_merge_md.py",
            "step5_convert_html.py",
            "step6_generate_toc.py",
            "requirements.txt",
            "template.html",
            "README.md"
        ]
        
        for filename in required_files:
            file_path = self.project_root / filename
            self.assertTrue(file_path.exists(), f"Required file {filename} is missing")
    
    def test_python_files_executable(self):
        """Test that Python files have execute permissions."""
        python_files = [
            "main.py",
            "step1_init.py",
            "step2_split_pdf.py",
            "step3_translate.py", 
            "step4_merge_md.py",
            "step5_convert_html.py",
            "step6_generate_toc.py"
        ]
        
        for filename in python_files:
            file_path = self.project_root / filename
            # Check if file has execute permission
            self.assertTrue(os.access(file_path, os.X_OK), 
                          f"Python file {filename} is not executable")


class TestConfigurationHandling(unittest.TestCase):
    """Test configuration loading and handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "config.txt"
        
        # Create test config file
        config_content = """INPUT_FILE=/path/to/test.pdf
INPUT_LANG=en
OUTPUT_LANG=zh
TEMP_DIR=/tmp/test_temp"""
        
        with open(self.config_file, 'w') as f:
            f.write(config_content)
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    def test_config_file_format(self):
        """Test config file format is correct."""
        config = {}
        
        with open(self.config_file, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    config[key] = value
        
        expected_keys = ['INPUT_FILE', 'INPUT_LANG', 'OUTPUT_LANG', 'TEMP_DIR']
        
        for key in expected_keys:
            self.assertIn(key, config, f"Config key {key} is missing")
        
        self.assertEqual(config['INPUT_LANG'], 'en')
        self.assertEqual(config['OUTPUT_LANG'], 'zh')


if __name__ == '__main__':
    unittest.main()