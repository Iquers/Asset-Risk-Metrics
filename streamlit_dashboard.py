import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Risk Metrics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def fetch_data(ticker, start_date, end_date):
    """Fetch stock data from Yahoo Finance"""
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False, progress=False)
        if stock_data.empty:
            st.error(f"No data found for {ticker}. Please check the ticker symbol.")
            return None
        
        # Handle MultiIndex columns from yfinance (when downloading multiple tickers)
        if isinstance(stock_data.columns, pd.MultiIndex):
            # For MultiIndex columns, get the first column that contains 'Adj Close' or 'Close'
            for col in stock_data.columns:
                if col[0] == 'Adj Close':
                    data = stock_data[col].copy()
                    data.name = ticker  # Set simple name for alignment
                    return data
            for col in stock_data.columns:
                if col[0] == 'Close':
                    data = stock_data[col].copy()
                    data.name = ticker
                    return data
        else:
            # Regular columns (single ticker download)
            if 'Adj Close' in stock_data.columns:
                data = stock_data['Adj Close'].copy()
                data.name = ticker
                return data
            elif 'Close' in stock_data.columns:
                data = stock_data['Close'].copy()
                data.name = ticker
                return data
        
        st.error(f"No suitable price column found for {ticker}")
        return None
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None


def calculate_daily_returns(data):
    """Calculate daily returns"""
    if data is None:
        return pd.Series()
    
    # If it's a DataFrame, try to extract the first column
    if isinstance(data, pd.DataFrame):
        if len(data.columns) > 0:
            data = data.iloc[:, 0]
        else:
            return pd.Series()
    
    # Now data should be a Series
    if not data.empty and len(data) > 0:
        returns = data.pct_change().dropna()
        return returns
    return pd.Series()


def calculate_beta(stock_returns, benchmark_returns):
    """Calculate beta"""
    try:
        if len(stock_returns) > 1 and len(benchmark_returns) > 1:
            stock_vals = np.array(stock_returns.values, dtype=float)
            benchmark_vals = np.array(benchmark_returns.values, dtype=float)
            covariance = np.cov(stock_vals, benchmark_vals)[0, 1]
            variance = np.var(benchmark_vals)
            if variance > 0:
                return float(covariance / variance)
    except (ValueError, TypeError, RuntimeError):
        pass
    return 0


def calculate_alpha(stock_returns, benchmark_returns, beta, risk_free_rate):
    """Calculate alpha"""
    try:
        if len(stock_returns) > 1 and len(benchmark_returns) > 1:
            stock_vals = np.array(stock_returns.values, dtype=float)
            benchmark_vals = np.array(benchmark_returns.values, dtype=float)
            stock_annualized_return = np.mean(stock_vals) * 252
            benchmark_annualized_return = np.mean(benchmark_vals) * 252
            alpha = stock_annualized_return - \
                (risk_free_rate + beta * (benchmark_annualized_return - risk_free_rate))
            return float(alpha)
    except (ValueError, TypeError, RuntimeError):
        pass
    return 0


def calculate_var(returns, percentile):
    """Calculate Value at Risk"""
    if returns is not None and len(returns) > 0:
        returns_array = np.array(returns.values, dtype=float)
        if len(returns_array) > 0:
            return np.percentile(returns_array, percentile)
    return 0


def calculate_sharpe_ratio(returns, risk_free_rate):
    """Calculate Sharpe Ratio"""
    try:
        returns_vals = np.array(returns.values, dtype=float)
        if len(returns_vals) < 2:
            return 0
        excess_returns = returns_vals - risk_free_rate
        std_excess = float(np.std(excess_returns))
        if std_excess > 0:
            return np.mean(excess_returns) / std_excess
    except (ValueError, TypeError, RuntimeWarning):
        return 0
    return 0


def calculate_volatility(returns):
    """Calculate volatility (annualized)"""
    try:
        returns_vals = np.array(returns.values, dtype=float)
        if len(returns_vals) < 2:
            return 0
        return np.std(returns_vals) * np.sqrt(252)
    except (ValueError, TypeError, RuntimeWarning):
        return 0


def calculate_max_drawdown(adjusted_close_prices):
    """Calculate maximum drawdown"""
    try:
        # Handle DataFrames by extracting first column
        if isinstance(adjusted_close_prices, pd.DataFrame):
            if len(adjusted_close_prices.columns) > 0:
                adjusted_close_prices = adjusted_close_prices.iloc[:, 0]
            else:
                return 0
        
        # Calculate the cumulative returns
        cumulative_returns = (1 + adjusted_close_prices.pct_change()).cumprod()
        # Calculate the cumulative max
        cumulative_max = cumulative_returns.cummax()
        # Calculate drawdown
        drawdown = (cumulative_returns - cumulative_max) / cumulative_max
        return drawdown.min()
    except Exception:
        return 0


def calculate_cagr(prices):
    """Calculate Compound Annual Growth Rate"""
    if len(prices) > 1:
        try:
            initial_price = float(prices.iloc[0])
            final_price = float(prices.iloc[-1])
            n_years = len(prices) / 252
            if n_years > 0 and initial_price > 0:
                return (final_price / initial_price) ** (1 / n_years) - 1
        except (ValueError, TypeError):
            return 0
    return 0


def normalize_data(data):
    """Normalize data to start at 1"""
    # Handle DataFrames by extracting first column
    if isinstance(data, pd.DataFrame):
        if len(data.columns) > 0:
            data = data.iloc[:, 0]
        else:
            return data
    
    if len(data) > 0 and data.iloc[0] > 0:
        return data / data.iloc[0]
    return data


def align_data(stock_data, benchmark_data):
    """Align stock and benchmark data by dates"""
    return stock_data.align(benchmark_data, join='inner')


def plot_comparison(stock_data, benchmark_data, stock_ticker, benchmark_ticker):
    """Plot stock vs benchmark comparison using Plotly"""
    normalized_stock = normalize_data(stock_data)
    normalized_benchmark = normalize_data(benchmark_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=normalized_stock.index,
        y=normalized_stock.values,
        name=stock_ticker,
        line=dict(width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=normalized_benchmark.index,
        y=normalized_benchmark.values,
        name=benchmark_ticker,
        line=dict(width=2)
    ))
    
    fig.update_layout(
        title=f"{stock_ticker} vs {benchmark_ticker} Performance",
        xaxis_title="Date",
        yaxis_title="Normalized Price (Starting Value = 1)",
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    
    return fig


def plot_returns_distribution(stock_returns, benchmark_returns, stock_ticker, benchmark_ticker):
    """Plot returns distribution"""
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=stock_returns.values,
        name=stock_ticker,
        opacity=0.7,
        nbinsx=50
    ))
    
    fig.add_trace(go.Histogram(
        x=benchmark_returns.values,
        name=benchmark_ticker,
        opacity=0.7,
        nbinsx=50
    ))
    
    fig.update_layout(
        title="Daily Returns Distribution",
        xaxis_title="Daily Returns",
        yaxis_title="Frequency",
        barmode='overlay',
        template='plotly_white',
        height=500
    )
    
    return fig


def plot_cumulative_returns(stock_returns, benchmark_returns, stock_ticker, benchmark_ticker):
    """Plot cumulative returns"""
    stock_cumulative = (1 + stock_returns).cumprod()
    benchmark_cumulative = (1 + benchmark_returns).cumprod()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=stock_cumulative.index,
        y=stock_cumulative.values,
        name=f"{stock_ticker} Cumulative Returns",
        fill='tozeroy'
    ))
    
    fig.add_trace(go.Scatter(
        x=benchmark_cumulative.index,
        y=benchmark_cumulative.values,
        name=f"{benchmark_ticker} Cumulative Returns",
        fill='tozeroy'
    ))
    
    fig.update_layout(
        title="Cumulative Returns",
        xaxis_title="Date",
        yaxis_title="Cumulative Return Multiplier",
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    
    return fig


def plot_drawdown(prices, ticker):
    """Plot drawdown over time"""
    cumulative_returns = (1 + prices.pct_change()).cumprod()
    cumulative_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns - cumulative_max) / cumulative_max
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=drawdown.index,
        y=drawdown.values,
        fill='tozeroy',
        name='Drawdown',
        line=dict(color='red')
    ))
    
    fig.update_layout(
        title=f"{ticker} Drawdown",
        xaxis_title="Date",
        yaxis_title="Drawdown",
        template='plotly_white',
        height=400
    )
    
    return fig


# Sidebar Configuration
st.sidebar.title("⚙️ Configuration")

col1, col2 = st.sidebar.columns(2)
with col1:
    stock_ticker = st.text_input("Stock Ticker", value="AAPL", key="stock_ticker").upper()
with col2:
    benchmark_ticker = st.text_input("Benchmark Ticker", value="^GSPC", key="benchmark_ticker").upper()

# Date range
end_date = st.sidebar.date_input("End Date", value=datetime.now())
start_date = st.sidebar.date_input("Start Date", value=datetime.now() - timedelta(days=365))

# Risk-free rate
risk_free_rate = st.sidebar.slider(
    "Risk-Free Rate (%)",
    min_value=0.0,
    max_value=10.0,
    value=4.5,
    step=0.1
) / 100

# Fetch and process data
if st.sidebar.button("📈 Calculate Metrics", use_container_width=True):
    st.session_state.calculate = True

if "calculate" in st.session_state and st.session_state.calculate:
    with st.spinner("Fetching data and calculating metrics..."):
        stock_data = fetch_data(stock_ticker, start_date, end_date)
        benchmark_data = fetch_data(benchmark_ticker, start_date, end_date)
        
        if stock_data is not None and benchmark_data is not None:
            # Align data
            stock_data, benchmark_data = align_data(stock_data, benchmark_data)
            
            # Calculate returns
            stock_returns = calculate_daily_returns(stock_data)
            benchmark_returns = calculate_daily_returns(benchmark_data)
            
            # Validate that we have enough data
            if len(stock_returns) == 0 or len(benchmark_returns) == 0:
                st.error("Not enough data available for the selected date range. Please try a longer period or different tickers.")
                # Debug info
                with st.expander("🔍 Debug Information"):
                    st.write(f"Stock data points: {len(stock_data)}")
                    st.write(f"Benchmark data points: {len(benchmark_data)}")
                    st.write(f"Stock returns: {len(stock_returns)}")
                    st.write(f"Benchmark returns: {len(benchmark_returns)}")
            else:
                # Debug info
                with st.expander("🔍 Debug Information"):
                    st.write(f"Stock data points: {len(stock_data)}")
                    st.write(f"Benchmark data points: {len(benchmark_data)}")
                    st.write(f"Stock returns: {len(stock_returns)}")
                    st.write(f"Benchmark returns: {len(benchmark_returns)}")
                    st.write(f"Stock returns sample: {stock_returns.head()}")
                    st.write(f"Benchmark returns sample: {benchmark_returns.head()}")
                
                # Calculate metrics
                beta = calculate_beta(stock_returns, benchmark_returns)
                alpha = calculate_alpha(stock_returns, benchmark_returns, beta, risk_free_rate)
                var_95 = calculate_var(stock_returns, 5)
                var_99 = calculate_var(stock_returns, 1)
                sharpe_ratio = calculate_sharpe_ratio(stock_returns, risk_free_rate / 252)
                volatility = calculate_volatility(stock_returns)
                max_drawdown = calculate_max_drawdown(stock_data)
                cagr = calculate_cagr(stock_data)
                
                # Display title and description
                st.title("📊 Risk Metrics Dashboard")
                st.markdown(f"**Analysis Period**: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
                
                # Key Metrics Section
                st.header("📌 Key Risk Metrics")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Beta", f"{beta:.4f}", 
                             help="Volatility relative to benchmark. >1 = more volatile")
                with col2:
                    st.metric("Alpha", f"{alpha:.4f}", 
                             help="Excess return vs benchmark")
                with col3:
                    st.metric("Sharpe Ratio", f"{sharpe_ratio:.4f}",
                             help="Risk-adjusted return (higher is better)")
                with col4:
                    st.metric("Max Drawdown", f"{max_drawdown:.2%}",
                             help="Peak-to-trough decline")
                
                col5, col6, col7, col8 = st.columns(4)
                with col5:
                    st.metric("Volatility (Annual)", f"{volatility:.2%}",
                             help="Annualized standard deviation")
                with col6:
                    st.metric("CAGR", f"{cagr:.2%}",
                             help="Compound Annual Growth Rate")
                with col7:
                    st.metric("VaR 95%", f"{var_95:.4f}",
                             help="Value at Risk at 95% confidence")
                with col8:
                    st.metric("VaR 99%", f"{var_99:.4f}",
                             help="Value at Risk at 99% confidence")
                
                # Metrics Explanation
                st.divider()
                with st.expander("📚 Metrics Explanation"):
                    col_exp1, col_exp2 = st.columns(2)
                    with col_exp1:
                        st.write("""
                        - **Beta**: Measures systematic risk. β > 1 means more volatile than benchmark
                        - **Alpha**: Excess return after adjusting for risk taken
                        - **Sharpe Ratio**: Risk-adjusted return. Higher is better
                        - **Volatility**: Standard deviation of returns (annualized)
                        """)
                    with col_exp2:
                        st.write("""
                        - **CAGR**: Compound Annual Growth Rate
                        - **Max Drawdown**: Largest peak-to-trough decline
                        - **VaR 95%**: Expected maximum daily loss 95% of the time
                        - **VaR 99%**: Expected maximum daily loss 99% of the time
                        """)
                
                # Charts Section
                st.header("📈 Performance Charts")
                
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "Price Comparison",
                    "Returns Distribution",
                    "Cumulative Returns",
                    "Drawdown Analysis",
                    "Summary Table"
                ])
                
                with tab1:
                    st.plotly_chart(
                        plot_comparison(stock_data, benchmark_data, stock_ticker, benchmark_ticker),
                        use_container_width=True
                    )
                
                with tab2:
                    st.plotly_chart(
                        plot_returns_distribution(stock_returns, benchmark_returns, stock_ticker, benchmark_ticker),
                        use_container_width=True
                    )
                
                with tab3:
                    st.plotly_chart(
                        plot_cumulative_returns(stock_returns, benchmark_returns, stock_ticker, benchmark_ticker),
                        use_container_width=True
                    )
                
                with tab4:
                    col_dd1, col_dd2 = st.columns(2)
                    with col_dd1:
                        st.plotly_chart(
                            plot_drawdown(stock_data, stock_ticker),
                            use_container_width=True
                        )
                    with col_dd2:
                        st.plotly_chart(
                            plot_drawdown(benchmark_data, benchmark_ticker),
                            use_container_width=True
                        )
                
                with tab5:
                    # Create summary table
                    summary_data = {
                        'Metric': [
                            'Beta', 'Alpha', 'Sharpe Ratio', 'Volatility (Annual)',
                            'CAGR', 'Max Drawdown', 'VaR 95%', 'VaR 99%'
                        ],
                        'Value': [
                            f"{beta:.4f}",
                            f"{alpha:.4f}",
                            f"{sharpe_ratio:.4f}",
                            f"{volatility:.4f}",
                            f"{cagr:.4f}",
                            f"{max_drawdown:.4f}",
                            f"{var_95:.4f}",
                            f"{var_99:.4f}"
                        ]
                    }
                    
                    summary_df = pd.DataFrame(summary_data)
                    st.dataframe(summary_df, use_container_width=True, hide_index=True)
                    
                    # Download button for results
                    csv = summary_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name=f"risk_metrics_{stock_ticker}_{end_date.strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )

else:
    st.title("📊 Risk Metrics Dashboard")
    st.info("👈 Enter your parameters in the sidebar and click 'Calculate Metrics' to begin!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Stock Ticker", stock_ticker)
    with col2:
        st.metric("Benchmark", benchmark_ticker)
    with col3:
        st.metric("Risk-Free Rate", f"{risk_free_rate:.1%}")
