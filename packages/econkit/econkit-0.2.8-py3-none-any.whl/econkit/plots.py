import matplotlib.pyplot as plt

def scatter(portfolio_returns):
    """
    Plot the mean against the standard deviation of portfolio returns.

    :param portfolio_returns: DataFrame containing the returns for each portfolio.
    """
    y_axis = portfolio_returns.mean()
    x_axis = portfolio_returns.std()

    plt.figure(figsize=(10, 6))
    plt.scatter(x_axis, y_axis)
    plt.xlabel('Volatility')
    plt.ylabel('Excepted Returns')

    # Annotate each point with its portfolio name
    for i, txt in enumerate(portfolio_returns.columns):
        plt.annotate(txt, (x_axis[i], y_axis[i]))

    plt.grid(True)
    plt.show()
    return(portfolio_returns)

