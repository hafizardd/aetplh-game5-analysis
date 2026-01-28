# AGENTS.md

Guidelines for agentic coding agents working in this repository.

## Project Overview

This is a Python data analysis project for YouTube live chat game analysis. It includes:
- **Main project**: Data analysis using numpy, pandas, matplotlib, seaborn
- **youtube-live-scrapers**: A git submodule for scraping YouTube live chat data
- **Notebooks**: Jupyter notebooks in `notebooks/` for interactive analysis

Python version: **3.10+** (required by youtube-live-scrapers submodule)

## Build/Lint/Test Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Install youtube-live-scrapers in development mode
pip install -e youtube-live-scrapers/
```

### Running Code
```bash
# Run the livechat scraper example
python youtube-live-scrapers/example.py <video_url>
python youtube-live-scrapers/example.py <video_url> <start_time> <end_time>

# Run Jupyter notebooks
jupyter notebook notebooks/scraping.ipynb
```

### Testing
```bash
# Run all tests with pytest
pytest

# Run a single test file
pytest tests/test_file.py

# Run a single test function
pytest tests/test_file.py::test_function_name

# Run tests matching a pattern
pytest -k "test_pattern"

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=. --cov-report=term-missing
```

### Code Quality
```bash
# Format with black (88 char line length)
black .

# Lint with flake8
flake8 . --max-line-length=88 --extend-ignore=E203

# Type checking with mypy
mypy . --ignore-missing-imports
```

## Code Style Guidelines

### Python Standards
- Follow PEP 8 with Black formatting (88 char line length)
- Use 4 spaces for indentation (no tabs)
- Use docstrings for all public functions and classes

### Import Organization
```python
# 1. Standard library imports
import sys
import json
import time
from math import floor
from typing import Optional, List, Dict

# 2. Third-party imports
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 3. Local imports
from livechat_scraper.scrapers import livechat_scraper
from livechat_scraper.constants import scraper_constants as sCons
```

### Type Hints
- Use type hints for all function parameters and return values
- Use `Optional[T]` for nullable parameters
```python
def process_data(data: pd.DataFrame, config: Dict[str, str]) -> Optional[pd.DataFrame]:
    """Process the input data according to configuration."""
    pass
```

### Naming Conventions
- **Variables/functions**: snake_case (`video_url`, `parse_time_to_ms`)
- **Classes**: PascalCase (`LiveChatScraper`, `PlayerState`)
- **Constants**: UPPER_SNAKE_CASE (`CONTINUATION_FETCH_BASE_URL`)
- **Private methods**: double underscore prefix (`__extract_video_id`)
- **Module-level private**: single underscore prefix

### Docstrings (Google Style)
```python
def parse_time_to_ms(time_str: str) -> int:
    """Convert time string to milliseconds.
    
    Args:
        time_str: Time string like '1:30:00' (1h 30m) or '5:30' (5m 30s)
    
    Returns:
        Time in milliseconds
    
    Raises:
        ValueError: If the time string format is invalid
    """
```

### Error Handling
- Use specific exceptions, not bare `except:`
- Include meaningful error messages with context
- Use try-except for external operations (network, file I/O)
- Always use timeouts for network requests
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Failed to fetch data from {url}: {e}")
    return None
```

## File Organization
```
aetplh-game5-analysis/
├── notebooks/               # Jupyter notebooks for analysis
│   ├── scraping.ipynb      # Live chat scraping workflow
│   ├── json_to_csv.ipynb   # Data conversion
│   └── sentiment.ipynb     # Sentiment analysis
├── youtube-live-scrapers/   # Git submodule for scraping
│   ├── livechat_scraper/
│   │   ├── scrapers/       # Scraper classes
│   │   ├── parsers/        # Response parsers
│   │   ├── requestors/     # HTTP request handlers
│   │   ├── builders/       # Data builders
│   │   ├── generators/     # Output generators
│   │   └── constants/      # Constants and config
│   └── example.py          # Usage examples
├── data/
│   ├── raw/                # Raw scraped JSON files
│   └── processed/          # Processed CSV files
├── requirements.txt        # Project dependencies
└── AGENTS.md              # This file
```

## Git Workflow
- Commit format: `type(scope): description`
- Types: feat, fix, docs, style, refactor, test, chore
- Never commit: `.venv/`, `__pycache__/`, API keys, `.env` files
- Keep commits focused and atomic

## Security
- Never commit API keys or credentials
- Use environment variables for sensitive config
- Validate all external data inputs

## Performance Tips
- Use vectorized numpy/pandas operations over loops
- Consider memory usage for large datasets
- Profile code with `cProfile` when performance is critical
