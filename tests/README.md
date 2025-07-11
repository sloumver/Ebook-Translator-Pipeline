# Test files for the Ebook Translator Pipeline

This directory contains unit tests for the ebook translation pipeline modules.

## Running Tests

Run all tests:
```bash
python -m pytest tests/
```

Run with coverage:
```bash
python -m pytest tests/ --cov=. --cov-report=html
```

Run specific test:
```bash
python -m pytest tests/test_pipeline.py::TestStep1Init::test_create_temp_directory
```

## Test Structure

- `test_pipeline.py`: Main test suite covering all pipeline modules
- Tests include:
  - Environment initialization
  - Configuration handling  
  - File structure validation
  - Utility functions
  - Project integrity checks

## Test Categories

1. **Unit Tests**: Test individual functions and methods
2. **Integration Tests**: Test component interactions
3. **Structure Tests**: Validate project file organization
4. **Configuration Tests**: Test config file handling

## Adding New Tests

When adding new features, please include corresponding tests:

```python
class TestNewFeature(unittest.TestCase):
    def test_new_functionality(self):
        # Test implementation
        pass
```