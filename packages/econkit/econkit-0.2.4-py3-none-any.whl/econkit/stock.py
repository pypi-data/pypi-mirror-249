import pandas as pd
import yfinance as yf
from datetime import datetime
import os

def stock(ticker_symbol: str, start_date: str, end_date: str, interval: str) -> pd.DataFrame:
    """
    Download stock data and return as a pandas DataFrame.
    The data is saved in a CSV file within a specified folder named 'Stocks'.

    Parameters:
    ticker_symbol: The stock symbol (e.g., 'AAPL').
    start_date: The start date in DD-MM-YYYY format (e.g., '01-01-2020').
    end_date: The end date in DD-MM-YYYY format (e.g., '31-12-2020').
    interval: The data interval. Valid intervals include '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', 
              '1d', '5d', '1wk', '1mo', '3mo' (e.g., '1d' for daily data).
    """

    def convert_date_format(date_string):
        """
        Convert date from DD-MM-YYYY to YYYY-MM-DD format.
        """
        return datetime.strptime(date_string, '%d-%m-%Y').strftime('%Y-%m-%d')

    # Convert start and end dates to the correct format
    start_date = convert_date_format(start_date)
    end_date = convert_date_format(end_date)

    # Download stock data from Yahoo Finance
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date, interval=interval)

    # Calculate % growth of Adjusted Close price
    stock_data['Returns'] = stock_data['Adj Close'].pct_change() * 100

    # Define the folder name for storing CSV files
    folder_name = "Stocks"

    # Create the folder if it does not exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Construct file path for saving the CSV file
    file_name = f"{folder_name}/{ticker_symbol}.csv"

    # Save data to a CSV file in the specified folder
    stock_data.to_csv(file_name)

    # Return the DataFrame
    return stock_data

