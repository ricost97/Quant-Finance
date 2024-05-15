#  Import Necessary Libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.integrate import quad
import yfinance as yf

# Define the Heston Model's Characteristic Function

def heston_char_func(u, T, kappa, theta, sigma, rho, v0, r, q, S0):
    i = 1j
    lambda_ = rho * sigma * i * u
    d = np.sqrt((kappa - lambda_)**2 + (sigma**2) * (u**2 + i * u))
    g = (kappa - lambda_ - d) / (kappa - lambda_ + d)

    # D and C terms calculation
    D = (kappa - lambda_ - d) / (sigma**2) * ((1 - np.exp(-d * T)) / (1 - g * np.exp(-d * T)))
    C = (r * i * u * T) + (kappa * theta / sigma**2) * ((kappa - lambda_ - d) * T - 2 * np.log((1 - g * np.exp(-d * T)) / (1 - g)))

    # Final characteristic function calculation
    return np.exp(C + D * v0 + i * u * np.log(S0 * np.exp((r - q) * T)))

# Implement the Breeden-Litzenberger Formula

def risk_neutral_density(K, T, S0, r, q, kappa, theta, sigma, rho, v0):
    integrand = lambda u: np.real(np.exp(-1j*u*np.log(K)) * heston_char_func(u-1j, T, kappa, theta, sigma, rho, v0, r, q, S0) / (1j*u*heston_char_func(-1j, T, kappa, theta, sigma, rho, v0, r, q, S0)))
    integral = quad(integrand, 0, np.inf, limit=100)[0]
    return np.exp(-r*T) * integral / (np.pi)

def call_price_from_density(K, T, S0, r, q, kappa, theta, sigma, rho, v0):
    density = lambda K: risk_neutral_density(K, T, S0, r, q, kappa, theta, sigma, rho, v0)
    C = quad(lambda K: np.maximum(S0 - K, 0) * density(K), 0, S0*2, limit=100)[0]
    return np.exp(-r*T) * C

# Retrieve Option Data

def get_option_chain(ticker, exp_date):
    
    option_chain = ticker.option_chain(exp_date)
    calls = option_chain.calls
    puts = option_chain.puts
    return calls, puts

def compare_option_prices(ticker, exp_date):
    data = ticker.history(period="1d")
    S0 = data['Close'].iloc[-1]  # Get the most recent closing price

    r = 0.01  # Risk-free rate
    q = 0.02  # Dividend yield
    kappa = 1
    theta = 0.05
    sigma = 0.3
    rho = -0.5
    v0 = 0.05
    T = 1  # Time to expiration (in years)

    calls, _ = get_option_chain(ticker, exp_date)
    theoretical_prices = []
    market_prices = []
    strikes = []
    
    for _, row in calls.iterrows():
        K = row['strike']
        market_price = row['lastPrice'] * 100
        theo_price = call_price_from_density(K, T, S0, r, q, kappa, theta, sigma, rho, v0)
        theoretical_prices.append(theo_price)
        market_prices.append(market_price)
        strikes.append(K)
    
    plt.figure(figsize=(10, 6))
    plt.plot(strikes, theoretical_prices, 'r-', label='Theoretical Prices')
    plt.plot(strikes, market_prices, 'b--', label='Market Prices')
    plt.xlabel('Strike Price')
    plt.ylabel('Option Price')
    plt.title('Theoretical vs Market Option Prices')
    plt.legend()
    plt.show()

    return [theoretical_prices, market_prices]


ticker = yf.Ticker('SPY')

prices_SPY = compare_option_prices(ticker, "2024-04-18")

print("Yay")