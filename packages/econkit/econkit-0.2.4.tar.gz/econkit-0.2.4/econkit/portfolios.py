import pandas as pd


def portfolios(weights, returns):
    """
    Calculate the returns for each portfolio.

    :param weights: DataFrame containing the weights of each stock in each portfolio.
    :param returns: DataFrame containing the daily returns of each stock.
    :return: DataFrame containing the daily returns for each portfolio.
    """
    portfolio_returns = pd.DataFrame(index=returns.index)

    for portfolio in weights.columns:
        # Multiplying returns by weights and summing across stocks for each day
        portfolio_returns[portfolio] = (returns * weights[portfolio]).sum(axis=1)
        
    portfolio_returns = pd.DataFrame(portfolio_returns)
    return round(portfolio_returns,2)




