# Asset-Risk-Metrics Dashboard

Updated for better data visualization via streamlit. Local streamlit dashboard by now.

A comprehensive Python application for analyzing risk metrics of assets and their benchmarks. Includes both a command-line interface and an interactive **Streamlit dashboard** for visualizing risk metrics.

## Features

### Risk Metrics Calculated
- **Beta**: Systematic risk relative to benchmark
- **Alpha**: Excess return after risk adjustment
- **Sharpe Ratio**: Risk-adjusted return metric
- **Volatility**: Annualized standard deviation of returns
- **CAGR**: Compound Annual Growth Rate
- **Value at Risk (VaR)**: 95% and 99% confidence levels
- **Maximum Drawdown**: Peak-to-trough decline



## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup Instructions

1. **Clone or extract the project**
   ```bash
   cd Asset-Risk-Metrics
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # or
   source venv/bin/activate      # On macOS/Linux
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Option 1: Streamlit Dashboard (Recommended)

**Run the interactive dashboard:**
```bash
streamlit run streamlit_dashboard.py
```

The dashboard will open in your browser (typically at `http://localhost:8501`).

**Steps:**
1. Enter the stock ticker (e.g., AAPL)
2. Enter the benchmark ticker (e.g., ^GSPC for S&P 500)
3. Select the start and end dates
4. Set the risk-free rate (e.g., 4.5% for US Treasury rate)
5. Click "📈 Calculate Metrics"
6. Explore the charts and download results

### Option 2: Command-Line Interface

**Run the original script:**
```bash
python "Asset risk report"
```

The script will prompt you for:
- Asset ticker symbol
- Benchmark ticker symbol
- Start date (YYYY-MM-DD)
- End date (YYYY-MM-DD)
- Risk-free rate (as a decimal, e.g., 0.045 for 4.5%)

## Ticker Symbols Reference

Common ticker symbols from Yahoo Finance:

**Stock Tickers:**
- AAPL - Apple Inc.
- MSFT - Microsoft Corporation
- GOOGL - Google/Alphabet
- TSLA - Tesla Inc.
- AMZN - Amazon

**Index Benchmarks:**
- ^GSPC - S&P 500
- ^IXIC - NASDAQ Composite
- ^DJI - Dow Jones Industrial Average
- ^FTSE - FTSE 100 (UK)
- ^N225 - Nikkei 225 (Japan)

## Project Structure

```
Asset-Risk-Metrics/
├── Asset risk report      # Original CLI script
├── streamlit_dashboard.py # Interactive Streamlit dashboard
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Dependencies

| Package | Purpose |
|---------|---------|
| numpy | Numerical calculations |
| pandas | Data manipulation |
| yfinance | Fetch stock data from Yahoo Finance |
| matplotlib | Static plotting (CLI) |
| streamlit | Web app framework |
| plotly | Interactive visualizations |

## Examples

### Example 1: Apple vs S&P 500
- Stock Ticker: AAPL
- Benchmark: ^GSPC
- Period: Last 2 years
- Risk-Free Rate: 4.5%

### Example 2: Tesla vs NASDAQ
- Stock Ticker: TSLA
- Benchmark: ^IXIC
- Period: Last 5 years
- Risk-Free Rate: 4.5%

## Metrics Interpretation

### Beta
- β = 1: Stock moves with benchmark
- β > 1: Stock is more volatile than benchmark
- β < 1: Stock is less volatile than benchmark

### Sharpe Ratio
- Measures risk-adjusted return
- Higher values indicate better risk-adjusted performance
- Typical good values: > 1.0

### Maximum Drawdown
- Represents the largest percentage decline from peak
- Lower (more negative) values indicate higher risk
- Important for understanding worst-case scenarios

### Volatility
- Annual standard deviation of returns
- Higher = more price fluctuation
- Lower = more stable returns

## Troubleshooting

### "No data found for ticker"
- Verify the ticker symbol is correct (check Yahoo Finance)
- Ensure the date range is valid
- Try a different date range

### Port already in use error
- Streamlit uses port 8501 by default
- Use: `streamlit run streamlit_dashboard.py --server.port 8502`

### Module not found error
- Ensure all packages are installed: `pip install -r requirements.txt`
- Check you're using the correct virtual environment

## Notes

- Data is sourced from Yahoo Finance (daily adjusted close prices)
- Risk-free rate is typically set to current US Treasury 1-year or 10-year rate
- All returns are annualized where applicable
- Date alignment ensures both assets have data for the entire period
- Caching is used to improve performance for repeated analyses
