import pandas as pd

def portfolios(weights, returns):
    """
    Calculate the returns for each portfolio.

    :param weights: DataFrame containing the weights of each stock in each portfolio.
    :param returns: DataFrame containing the daily returns of each stock.
    :return: DataFrame containing the daily returns for each portfolio.
    """
    # Using list comprehension to calculate portfolio returns
    portfolio_returns = pd.concat([(returns * weights[col]).sum(axis=1) for col in weights.columns], axis=1)
    
    # Setting column names to portfolio names
    portfolio_returns.columns = weights.columns

    # Rounding the returns to two decimal places
    return round(portfolio_returns, 2)

