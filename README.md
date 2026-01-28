# AE vs TL PH Game 5 Analysis

A Python data analysis project for analyzing YouTube live chat data from the M7 World Championship Knockout Stage (Alter Ego vs Team Liquid PH Game 5). This project scrapes, processes, and performs sentiment analysis on live chat messages during esports matches.

## Data Source

**YouTube Live Replay**: [LIVE KNOCKOUT STAGE HARI 5 - M7 World Championship (ID)](https://www.youtube.com/watch?v=cQIz9A5S2jU)

- **Scraped Time Range**: 3:25:30 to 3:52:40 (Game 5 duration)
- **Messages Collected**: ~16,800 live chat messages
- **Language**: Primarily Indonesian

## Features

- **Live Chat Scraping**: Scrape YouTube live chat messages from VODs with time range support using [youtube-livechat-scraper](https://github.com/ohn0/youtube-livechat-scrapers)
- **Data Processing**: Convert raw JSON data to structured CSV format with emoji extraction
- **Indonesian Text Normalization**: Handle informal Indonesian text/slang (214+ terms) using custom dictionary and PySastrawi
- **Sentiment Analysis**: Analyze viewer sentiment using transformer models (HuggingFace)
- **Event Correlation**: Map 22 in-game events (kills, lords, wars) to chat reactions
- **Time-based Analysis**: Correlate chat activity with key game moments

## Project Structure

```
aetplh-game5-analysis/
├── notebooks/                  # Jupyter notebooks for analysis
│   ├── scraping.ipynb         # Live chat scraping workflow
│   ├── json_to_csv.ipynb      # JSON to CSV data conversion
│   └── sentiment.ipynb        # Sentiment analysis and visualization
├── youtube-live-scrapers/      # Git submodule (fork of ohn0/youtube-livechat-scrapers)
├── data/
│   ├── raw/                   # Raw scraped JSON files
│   ├── processed/             # Processed CSV files (comments, events, sentiment)
│   └── slang_dict.json        # Indonesian slang normalization dictionary
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

video_url = "https://www.youtube.com/watch?v=cQIz9A5S2jU"
scraper = livechat_scraper.LiveChatScraper(
    video_url,
    start_time="3:25:30",  # Draft phase start
    end_time="3:52:40"     # Post-match highlights
)

scraper.scrape()
scraper.write_to_file(sCons.OUTPUT_JSON, "output_filename", output_path="../data/raw")
```

### 2. Processing Data

Use the `json_to_csv.ipynb` notebook to convert raw JSON data to CSV format, extracting message content, emojis, and text.

### 3. Sentiment Analysis

Use the `sentiment.ipynb` notebook to:
- Normalize timestamps relative to game start
- Apply Indonesian slang normalization
- Correlate chat messages with in-game events
- Analyze viewer sentiment patterns with transformer models

## Dependencies

- **Data Analysis**: numpy, pandas, matplotlib, seaborn
- **NLP/ML**: transformers, torch, PySastrawi (Indonesian stemmer)
- **Web Scraping**: requests, beautifulsoup4
- **Notebooks**: ipykernel

## Acknowledgments

- **YouTube Live Chat Scraper**: Based on [ohn0/youtube-livechat-scrapers](https://github.com/ohn0/youtube-livechat-scrapers) - A tool to scrape YouTube live chat data including chat messages, superchats, memberships, and stickers
- **M7 World Championship**: Mobile Legends: Bang Bang esports tournament

## License

This project is for educational and research purposes.