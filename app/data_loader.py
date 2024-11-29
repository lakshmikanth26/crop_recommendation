import os
import pandas as pd

# Function to load data from the 'data' folder (relative to app directory)
def load_data(filename):
    file_path = os.path.join(os.path.dirname(__file__), 'data', filename)
    return pd.read_csv(file_path)

# Example of loading crop_yield.csv
def load_crop_yield_data():
    return load_data('crop_yield.csv')

# Example of loading crop_price.csv
def load_crop_price_data():
    return load_data('crop_price.csv')

# Function to load other data files similarly
def load_crop_varieties_data():
    return load_data('crop_varieties.csv')

def load_india_rainfall_data():
    return load_data('India_rainfall.csv')

# Main function to load all data
def load_and_clean_data():
    crop_yield_data = load_crop_yield_data()
    crop_price_data = load_crop_price_data()
    crop_varieties_data = load_crop_varieties_data()
    india_rainfall_data = load_india_rainfall_data()

    # Apply any cleaning function here
    return crop_yield_data, crop_price_data, crop_varieties_data, india_rainfall_data
