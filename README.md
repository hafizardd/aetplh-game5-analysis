# AE vs TL PH Game 5 Analysis

A Python data analysis project for analyzing YouTube live chat data from the M7 World Championship Knockout Stage (Alter Ego vs Team Liquid PH Game 5). This project scrapes, processes, and performs sentiment analysis on live chat messages during esports matches.

## Features

- **Live Chat Scraping**: Scrape YouTube live chat messages from VODs with time range support
- **Data Processing**: Convert raw JSON data to structured CSV format
- **Sentiment Analysis**: Analyze viewer sentiment and reactions during key game moments
- **Time-based Analysis**: Correlate chat activity with in-game events

## Project Structure

```
aetplh-game5-analysis/
├── notebooks/                  # Jupyter notebooks for analysis
│   ├── scraping.ipynb         # Live chat scraping workflow
│   ├── json_to_csv.ipynb      # JSON to CSV data conversion
│   └── sentiment.ipynb        # Sentiment analysis and visualization
├── youtube-live-scrapers/      # Git submodule for YouTube scraping
├── data/
│   ├── raw/                   # Raw scraped JSON files
│   └── processed/             # Processed CSV files
├── requirements.txt           # Project dependencies
├── AGENTS.md                  # Guidelines for AI coding agents
└── README.md                  # This file
```

## Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository with submodules:
   ```bash
   git clone --recurse-submodules https://github.com/hafizardd/aetplh-game5-analysis.git
   cd aetplh-game5-analysis
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e youtube-live-scrapers/
   ```

## Usage

### 1. Scraping Live Chat Data

Use the `scraping.ipynb` notebook to scrape live chat messages from a YouTube VOD:

```python
from livechat_scraper.scrapers import livechat_scraper
from livechat_scraper.constants import scraper_constants as sCons

video_url = "https://www.youtube.com/watch?v=VIDEO_ID"
scraper = livechat_scraper.LiveChatScraper(
    video_url,
    start_time="3:25:30",  # Start timestamp
    end_time="3:52:40"     # End timestamp
)

scraper.scrape()
scraper.write_to_file(sCons.OUTPUT_JSON, "output_filename", output_path="../data/raw")
```

### 2. Processing Data

Use the `json_to_csv.ipynb` notebook to convert raw JSON data to CSV format, extracting message content, emojis, and text.

### 3. Sentiment Analysis

Use the `sentiment.ipynb` notebook to:
- Normalize timestamps relative to game start
- Correlate chat messages with in-game events
- Analyze viewer sentiment patterns

## Dependencies

- **Data Analysis**: numpy, pandas, matplotlib, seaborn
- **Machine Learning**: transformers, torch, scikit-learn
- **Web Scraping**: requests, beautifulsoup4
- **Notebooks**: ipykernel

## License

This project is for educational and research purposes.