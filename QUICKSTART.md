# Streamlit Dashboard - Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
Open PowerShell in the project folder and run:
```powershell
pip install -r requirements.txt
```

### Step 2: Run the Dashboard
```powershell
streamlit run streamlit_dashboard.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

### Step 3: Configure Your Analysis
1. **Stock Ticker**: Enter the company stock symbol (e.g., AAPL for Apple)
2. **Benchmark Ticker**: Enter index symbol (e.g., ^GSPC for S&P 500)
3. **Date Range**: Select start and end dates for analysis
4. **Risk-Free Rate**: Set the risk-free rate as a percentage
5. **Click Calculate**: Press the "📈 Calculate Metrics" button

## 📊 Dashboard Features

### Main Metrics Display
Shows 8 key risk metrics in card format with hover explanations:
- Beta, Alpha, Sharpe Ratio, Max Drawdown
- Volatility, CAGR, VaR 95%, VaR 99%

### Five Analysis Tabs

**Tab 1: Price Comparison**
- Normalized price comparison between your stock and benchmark
- Shows relative performance over the selected period

**Tab 2: Returns Distribution**
- Histogram showing daily returns distribution
- Compares volatility characteristics between assets

**Tab 3: Cumulative Returns**
- Overlaying cumulative return curves
- Easy visualization of compound growth

**Tab 4: Drawdown Analysis**
- Side-by-side drawdown charts
- Shows peak-to-trough declines over time

**Tab 5: Summary Table**
- All metrics in tabular format
- Includes CSV export button for further analysis

## 💡 Tips & Best Practices

### Popular Examples to Try

**Conservative Portfolio Analysis**
- Stock: XLE (Energy sector)
- Benchmark: ^GSPC (S&P 500)
- Shows defensive characteristics

**Growth Stock Analysis**
- Stock: TSLA (Tesla)
- Benchmark: ^IXIC (NASDAQ)
- Shows higher volatility/beta

**Dividend Stock Analysis**
- Stock: KO (Coca-Cola)
- Benchmark: ^GSPC (S&P 500)
- Shows stable, low-volatility performance

### Understanding Results

**Good Sharpe Ratio**: > 1.0 (excellent risk-adjusted returns)
**Low Drawdown**: Closer to 0% is better (less downside risk)
**Beta near 1**: Moves similarly to benchmark
**Positive Alpha**: Outperformance after risk adjustment

## 🔧 Troubleshooting

### Dashboard won't start?
```powershell
# Make sure streamlit is installed
pip install --upgrade streamlit

# Try specifying port explicitly
streamlit run streamlit_dashboard.py --server.port 8501
```

### "No data found for ticker"?
- Double-check ticker symbol on Yahoo Finance
- Try a more recent date range
- Some tickers may not have historical data

### Slow performance?
- Streamlit caches results automatically
- Shorter date ranges will be faster
- Refresh browser to clear cache if needed

## 📈 Next Steps

1. **Experiment with different tickers** to understand risk metrics
2. **Compare sector ETFs** against their benchmark indices
3. **Export results** as CSV for further analysis
4. **Adjust risk-free rate** based on current Treasury yields
5. **Use for portfolio analysis** by comparing multiple assets

## 📚 Resources

- **Yahoo Finance Tickers**: https://finance.yahoo.com/
- **US Treasury Rates**: https://www.treasury.gov/resource-center/data-chart-center/
- **Streamlit Documentation**: https://docs.streamlit.io/

## ⚡ Running in Background (Optional)

To keep the dashboard running:
```powershell
# Windows - Keep terminal open
streamlit run streamlit_dashboard.py

# Access from browser: http://localhost:8501
```

For deployment to cloud (Streamlit Cloud):
1. Push your code to GitHub
2. Go to https://share.streamlit.io/
3. Connect your repository
4. Follow deployment steps

---

Enjoy your interactive Risk Metrics Dashboard! 📊
