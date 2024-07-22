from pandas_datareader import data as pdr
import yfinance as yf
from diskcache import Cache
from datetime import datetime
from Stock import Stock
from Portfolio import Portfolio

# Override data reader with yfinance
yf.pdr_override()

# Efficient caching for data retrieval
cache = Cache('stock_data_cache')  # Specify a name for the cache on disk

def get_stock_data_cached(ticker, start_date, end_date):
    """Retrieves stock data from cache or calls Yahoo Finance API if needed."""
    cache_key = (ticker, start_date, end_date)
    if cache_key in cache:
        return cache[cache_key]  # Reuse cached data

    try:
        data = pdr.get_data_yahoo(ticker, start=start_date, end=end_date)
        cache[cache_key] = data  # Store retrieved data in disk cache
        return data
    except Exception as e:
        print(f"Error retrieving data for {ticker}: {e}")
        return None

"""def get_stock_data_cached2(ticker, start_date, end_date):
    #check if there is any data in the cache of the stock ticker
    cache_key = (ticker)
    if cache_key in cache:
        if cache[cache_key][1] == end_date:
            return cache[cache_key]
    try:
        data = pdr.get_data_yahoo(ticker, start=start_date, end=end_date)
        cache[cache_key] = [data, end_date]
        return [data, end_date]"""


def build_portfolio(tickers, weights, portfolio):
    """Retrieves stock data for multiple tickers and organizes it."""
    for index, ticker in enumerate(tickers):
        data = get_stock_data_cached(ticker, portfolio.start_date, portfolio.end_date)
        if data is not None:
            portfolio.add_stock(Stock(ticker, weights[index], data))
        else:
            print(f"Failed to retrieve data for {ticker}")


# Set tickers and date range
tickers = ['VGT', 'SOXX', 'VOO', 'SPY', 'QQQ']
weights = [0.3, 0.1, 0.3, 0.1, 0.2]
start_date = datetime(2022, 12, 1)
end_date = datetime(2023, 12, 15)

portfolio = Portfolio(10000, 2000, start_date, end_date)
# Retrieve and store stock data
build_portfolio(tickers, weights, portfolio)
portfolio.calculate_initial_portfolio()
portfolio.calculate_monthly_portfolio(datetime(2023, 1, 10))
total = portfolio.get_current_total_value()
print(total)
print("Total amount invested: ", portfolio.total_amount_invested)
