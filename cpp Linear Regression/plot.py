import numpy as np
import matplotlib.pyplot as plt

def load_coefficients(filename):
    with open(filename, 'r') as f:
        coefficients = np.array(f.read().strip().split(',')).astype(float)
    return coefficients

def predict(coefficients, x_values):
    # Prediction using y = b0 + b1 * x
    return coefficients[0] + coefficients[1] * x_values

def main():
    # Load the coefficients
    coefficients = load_coefficients("regression_coefficients.csv")
    
    # Define the range for the next day (assuming the last x_value was 100)
    x_values = np.linspace(101, 200, 100)  # Example x_values for the next day
    predictions = predict(coefficients, x_values)
    
    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(x_values, predictions, label='Predicted Stock Prices')
    plt.xlabel('Time')
    plt.ylabel('Predicted Stock Price')
    plt.title('Stock Price Prediction for the Next Day')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
