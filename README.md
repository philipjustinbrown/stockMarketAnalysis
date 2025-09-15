# Stock Market Analysis

A command-line tool for analyzing and visualizing stock market data for multiple tickers using Yahoo Finance.

## Features

- Download historical stock data for one or more tickers
- Interactive menu for selecting chart types and actions
- Line chart, area chart, and candlestick chart visualizations
- Moving average analysis (10-day and 20-day)
- Option to open a web page with a list of stock tickers

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/philipjustinbrown/stockMarketAnalysis.git
   cd stockMarketAnalysis
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Usage

Run the script from the command line:
```sh
python stockMarketAnalysis.py
```

Follow the prompts to:
- Select the type of analysis or chart
- Enter one or more stock tickers (e.g., `AAPL MSFT TSLA`)
- Specify the date range for analysis

## Requirements

- Python 3.7+
- See `requirements.txt` for required packages