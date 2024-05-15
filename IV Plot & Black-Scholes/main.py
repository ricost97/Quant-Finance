import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import yfinance as yf

# Black-Scholes Model
def black_scholes(S, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    Nd1 = norm.cdf(d1)
    Nd2 = norm.cdf(d2)
    Nd1n = norm.cdf(-d1)
    Nd2n = norm.cdf(-d2)
    if option_type == "call":
        return S * Nd1 - K * np.exp(-r * T) * Nd2
    else:
        return K * np.exp(-r * T) * Nd2n - S * Nd1n

def fetch_options_data(ticker):
    # Create a ticker object
    stock = yf.Ticker(ticker)

    # Get options expiration dates
    exp_dates = stock.options

    # Container for options data
    options_frames = []

    # Fetch options data for each expiration date
    for date in exp_dates:
        # Fetch call and put options
        opt = stock.option_chain(date)
        calls = opt.calls
        puts = opt.puts
        
        # Add an expiration date column
        calls['expiration'] = date
        puts['expiration'] = date
        
        # Combine call and put data
        options_data = pd.concat([calls, puts])
        options_frames.append(options_data)

    # Combine all data into a single DataFrame
    full_options_data = pd.concat(options_frames)
    
    return full_options_data

def plot_option_price_differences(ticker, start_date, end_date):
    # Fetch options data
    options_data = fetch_options_data(ticker)

    # Convert date strings to datetime objects
    options_data['expiration'] = pd.to_datetime(options_data['expiration'])

    # Filter data by ticker and date
    mask = (
    (options_data['expiration'] >= pd.to_datetime(start_date)) &
    (options_data['expiration'] <= pd.to_datetime(end_date)) &
    (options_data['contractSymbol'].str.contains('C')) &
    (options_data['strike'] <= 560) &
    (options_data['strike'] >= 500)
    )

    filtered_data = options_data[mask]

    # Ensure data types and presence of columns
    if 'lastPrice' in filtered_data.columns and 'strike' in filtered_data.columns:
        # Initialize lists to store results
        bs_prices = []
        price_differences = []

        # Iterate over rows to calculate Black-Scholes prices and differences
        for idx, row in filtered_data.iterrows():
            option_type = 'call' if 'C' in row['contractSymbol'] else 'put'
            bs_price = black_scholes(
                S=row['lastPrice'], 
                K=row['strike'], 
                T=(row['expiration'].day - pd.Timestamp.today().day) / 365.0,
                r=0.045,  # Example risk-free rate
                sigma=row['impliedVolatility'], 
                option_type=option_type
            )
            bs_prices.append(bs_price)
            price_differences.append(row['lastPrice'] - bs_price)

        # Assign results to DataFrame
        filtered_data['BS_price'] = bs_prices
        filtered_data['price_difference'] = price_differences

        # Plot the differences
        plt.figure(figsize=(10, 5))
        plt.scatter(filtered_data['strike'], filtered_data['impliedVolatility'], label='IV', marker='x')
        plt.title(f'IV for {ticker}')
        plt.xlabel('Strike Price')
        plt.ylabel('IV')
        plt.legend()
        plt.grid(True)
        plt.show()
        print("Done!")
    else:
        print("Required columns are missing from the data.")

# Call the function with the actual parameters
plot_option_price_differences('SPY', '2024-05-17', '2024-05-17')
