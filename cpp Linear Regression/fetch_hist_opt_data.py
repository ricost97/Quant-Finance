import yfinance as yf
import datetime

def get_option_data(stock_symbol, expiration_date, option_type, strike):
    stock = yf.Ticker(stock_symbol)
    option_chain = stock.option_chain(expiration_date)
    options = getattr(option_chain, "calls" if option_type.startswith("call") else "puts")
    option_data = options[options["strike"] == strike]
    return option_data

def get_option_history_data(contract_symbol, start_date, end_date):
    option = yf.Ticker(contract_symbol)
    option_history = option.history(start=start_date, end=end_date)
    return option_history

def main():
    stock_symbol = "AAPL"
    expiration_date = '2024-05-31'  # Set a specific expiration date
    option_type = "call"
    strike = 190.0

    option_data = get_option_data(stock_symbol, expiration_date, option_type, strike)
    
    # Ensure we have data to process
    if not option_data.empty:
        for i, od in option_data.iterrows():
            contract_symbol = od["contractSymbol"]
            option_info = yf.Ticker(contract_symbol).info
            option_expiration_date = datetime.datetime.fromtimestamp(option_info["expireDate"])
            
            # Setting the date range
            start_date = '2024-05-15'
            end_date = '2024-05-01'

            # Get historical data
            option_history = get_option_history_data(contract_symbol, start_date, end_date)
            if not option_history.empty:
                # Save the historical data to CSV
                csv_filename = f"{contract_symbol}_history.csv"
                option_history.to_csv(csv_filename)
                print(f"Saved historical data to {csv_filename}")
            else:
                print(f"No historical data available for {contract_symbol}")

if __name__ == "__main__":
    main()

    