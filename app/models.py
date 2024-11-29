import pandas as pd
import os

# Function to load data from the 'data' folder (relative to app directory)
def load_data(file_name):
    file_path = os.path.join(os.path.dirname(__file__), 'data', file_name)
    data = pd.read_csv(file_path)
    
    print(f"Columns: {data.columns}")  # Print column names to check
    print(f"First few rows: {data.head()}")  # Print the first few rows to check the data
    
    return data

# Function to filter crop yield data based on crop, state, and year
def get_filtered_data(crop, state, year):
    # Load crop yield data
    print(f"Filtering for crop: {crop}, state: {state}, year: {year}")  # Debugging
    yield_data = load_data('crop_yield.csv')

    yield_data['Crop'] = yield_data['Crop'].str.strip()
    yield_data['State'] = yield_data['State'].str.strip()

    crop = crop.strip()  # Strip input crop value as well
    state = state.strip()  # Strip input state value

    year = int(year)  # Ensure year is an integer for comparison

    filtered = yield_data[
        (yield_data['Crop'] == crop) &
        (yield_data['State'] == state) &
        (yield_data['Crop_Year'] == year)
    ]

    print(f"Filtered Data:\n{filtered.head()}")
    return filtered