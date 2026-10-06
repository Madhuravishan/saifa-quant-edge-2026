import yfinance as yf
import pandas as pd
import numpy as np

def download_data(config):
    tickers = config['data']['tickers']
    start_date = config['data']['start_date']
    end_date = config['data']['end_date']
    
    # Download adjusted close prices
    raw_data = yf.download(tickers, start=start_date, end=end_date)
    
    if 'Adj Close' in raw_data.columns:
        if isinstance(raw_data.columns, pd.MultiIndex):
            data = raw_data['Adj Close']
        else:
            data = raw_data[['Adj Close']]
    elif 'Close' in raw_data.columns:
        if isinstance(raw_data.columns, pd.MultiIndex):
            data = raw_data['Close']
        else:
            data = raw_data[['Close']]
    else:
        # Fallback for newer yfinance which might have Price in level 0
        try:
            data = raw_data.xs('Adj Close', level=0, axis=1)
        except:
            data = raw_data.xs('Close', level=0, axis=1)
    data = data.ffill().bfill()
    
    # Calculate simple returns (for portfolio aggregation) and log returns (for modeling)
    simple_returns = data.pct_change().dropna()
    log_returns = np.log(data / data.shift(1)).dropna()
    
    # Ensure columns match order in config
    simple_returns = simple_returns[tickers]
    log_returns = log_returns[tickers]
    
    return data, simple_returns, log_returns

def split_data(df, train_end_date):
    train = df.loc[:train_end_date]
    test = df.loc[train_end_date:]
    # Exclude overlap
    if len(test) > 0 and test.index[0] <= train.index[-1]:
        test = test.iloc[1:]
    return train, test
