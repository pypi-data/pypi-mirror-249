import plotly.express as px

def scatter(portfolio_returns):
    """
    Plot the mean against the standard deviation of portfolio returns using Plotly for interactivity.

    :param portfolio_returns: DataFrame containing the returns for each portfolio.
    """
    df = portfolio_returns.copy()
    df['Mean'] = df.mean(axis=1)
    df['Volatility'] = df.std(axis=1)
    df['Portfolio'] = df.index

    fig = px.scatter(df, x='Volatility', y='Mean', text='Portfolio', 
                     title='Portfolio Returns: Expected Returns vs Volatility',
                     labels={'Mean': 'Expected Returns', 'Volatility': 'Volatility'})
    fig.update_traces(textposition='top center')
    fig.update_layout(showlegend=False)
    fig.show()

