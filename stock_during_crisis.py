import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Default tickers
default_tickers = ['AAPL', 'SPY', 'KO', 'XOM', 'GLD']

# Define crisis dates
crisis_dates = {
    "COVID-19 Market Crash": ("2020-02-01", "2020-04-30"),
    "Global Financial Crisis": ("2008-10-01", "2009-03-31"),
    "Dot-com Bubble Burst": ("2000-03-01", "2002-10-31"),
    "Asian Financial Crisis": ("1997-07-01", "1998-01-31"),
    "Black Monday": ("1987-06-01", "1987-12-31"),
    "Savings and Loan Crisis": ("1986-01-01", "1995-12-31"),
    "1973-74 Stock Market Crash": ("1973-10-01", "1974-04-30")
}

st.write(
    '###### REMARK: Click the arrow icon in the top left corner to open the control sidebar, where you can select stock tickers and crisis events.')

# Function to fetch stock data from yfinance
def fetch_data(tickers, start_date, end_date):
    try:
        data = yf.download(tickers, start=start_date, end=end_date)["Adj Close"]
        return data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None


# Function to normalize data
def normalize_data(data):
    return data / data.iloc[0] * 100  # Normalize to 100


# Function to plot stock data for a specific crisis
def plot_crisis_data(crisis_name, start_date, end_date, tickers):
    data = fetch_data(tickers, start_date, end_date)

    if data is None:
        return  # If there's an error in fetching data, don't proceed with plotting

    # Check for valid tickers
    valid_tickers = data.columns
    invalid_tickers = [ticker for ticker in tickers if ticker not in valid_tickers]

    if invalid_tickers:
        st.error(f"Invalid tickers: {', '.join(invalid_tickers)}. Please enter valid tickers.")
        return

    normalized_data = normalize_data(data)

    plt.figure(figsize=(14, 7))
    for ticker in normalized_data.columns:
        plt.plot(normalized_data.index, normalized_data[ticker], label=ticker)

    plt.title(f'Stock Prices During {crisis_name}')
    plt.xlabel('Date')
    plt.ylabel('Normalized Price (%)')
    plt.axvline(pd.to_datetime(start_date), color='red', linestyle='--', label='Crisis Start')
    plt.axvline(pd.to_datetime(end_date), color='green', linestyle='--', label='Crisis End')
    plt.legend()
    plt.grid()

    st.pyplot(plt)


# Streamlit sidebar input for stock tickers (allow up to 5)
st.sidebar.title("Stock Selection")
tickers_input = st.sidebar.text_input(
    "Enter up to 5 stock tickers (separated by commas)",
    value="AAPL, SPY, KO, XOM, GLD"
)
tickers = [ticker.strip().upper() for ticker in tickers_input.split(',')]

# Limit to 5 tickers
if len(tickers) > 5:
    st.sidebar.warning("You can only select up to 5 tickers. The first 5 tickers will be used.")
    tickers = tickers[:5]

# Streamlit sidebar input for crisis selection
st.sidebar.title("Crisis Selection")
crisis_selected = st.sidebar.selectbox(
    "Select a crisis to view stock performance",
    list(crisis_dates.keys())
)

# Get selected crisis dates
start_date, end_date = crisis_dates[crisis_selected]

# Display the graph for the selected crisis and tickers
st.title(f"Stock Prices During {crisis_selected}")
plot_crisis_data(crisis_selected, start_date, end_date, tickers)

