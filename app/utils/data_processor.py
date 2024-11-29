import pandas as pd
import plotly.express as px

# Function to process crop yield data and rainfall data
def process_crop_yield_data(crop_yield_data, rainfall_data):
    # Check if the necessary columns exist in both datasets
    required_columns_crop_yield = ['Crop_Year', 'State', 'Yield', 'Annual_Rainfall']
    required_columns_rainfall = ['YEAR', 'Actual Rainfall: JUN']

    if not all(col in crop_yield_data.columns for col in required_columns_crop_yield):
        raise ValueError("Missing required columns in crop yield data")
    
    if not all(col in rainfall_data.columns for col in required_columns_rainfall):
        raise ValueError("Missing required columns in rainfall data")

    # Merge the data on common years
    merged_data = pd.merge(crop_yield_data, rainfall_data, left_on='Crop_Year', right_on='YEAR', how='inner')

    # Plot Crop Yield vs Rainfall
    fig = px.scatter(merged_data, x='Annual_Rainfall', y='Yield', color='State',
                     title='Crop Yield vs Rainfall Analysis by State',
                     labels={'Annual_Rainfall': 'Annual Rainfall (mm)', 'Yield': 'Crop Yield (Kg/Ha)'})
    return fig

# Function to process crop price data for a specific commodity
def process_crop_price_data(crop_price_data, crops=None):
    # If no specific crops are provided, use all crops
    if crops is None:
        crops = crop_price_data['Commodity'].unique()

    # Filter data for the selected crops
    crop_data = crop_price_data[crop_price_data['Commodity'].isin(crops)]

    # Check if the necessary columns exist
    required_columns_price = ['Arrival_Date', 'Modal_x0020_Price', 'Commodity']
    if not all(col in crop_data.columns for col in required_columns_price):
        raise ValueError("Missing required columns in the crop price data")

    # Convert Arrival_Date to datetime
    crop_data['Arrival_Date'] = pd.to_datetime(crop_data['Arrival_Date'], format='%d/%m/%Y')

    # Plot Crop Price Trends for all selected crops
    line_fig = px.line(crop_data, x='Arrival_Date', y='Modal_x0020_Price', color='Commodity', 
                  title='Crop Price Trends Over Time',
                  labels={'Arrival_Date': 'Date', 'Modal_x0020_Price': 'Price (INR)', 'Commodity': 'Crop'})
    
    box_fig = px.box(crop_data, x='Commodity', y='Modal_x0020_Price', points="all",
             title='Price Distribution per Commodity')

    bar_fig = px.bar(crop_data, x='State', y='Modal_x0020_Price', color='Commodity',
             title='Commodity Price Comparison by State')
    
    heatmap_fig = px.density_heatmap(crop_data, x="State", y="Commodity", z="Modal_x0020_Price", 
                         title="Price Heatmap by State and Commodity")

    return line_fig,box_fig,bar_fig,heatmap_fig

# Function to process rainfall data from a CSV file
def process_rainfall_data(file_path):
    # Load the rainfall data
    df = pd.read_csv(file_path)

    # Check for necessary columns in the rainfall data
    required_columns_rainfall = ['YEAR', 'Actual Rainfall: JUN', 'Actual Rainfall: JUL', 'Actual Rainfall: AUG', 'Actual Rainfall: SEPT']
    if not all(col in df.columns for col in required_columns_rainfall):
        raise ValueError("Missing required columns in the rainfall data")

    # Add any data processing steps here (e.g., calculating average rainfall by year)
    # Example: calculating average rainfall for June to September
    df['Avg_Rainfall'] = df[['Actual Rainfall: JUN', 'Actual Rainfall: JUL', 'Actual Rainfall: AUG', 'Actual Rainfall: SEPT']].mean(axis=1)

    return df

def process_crop_variety_data(crop_varieties_data):
    # Check if the necessary columns exist
    crop_varieties_data.columns = crop_varieties_data.columns.str.strip()
    required_columns_varieties = ['Type of Crops', 'Crops', 'Variety name', 'Year', 'Remarks/ development by']
    if not all(col in crop_varieties_data.columns for col in required_columns_varieties):
        raise ValueError("Missing required columns in the crop varieties data")

    # Group the data by 'Crops' and 'Variety name' to count the number of varieties for each crop
    variety_count = crop_varieties_data.groupby(['Crops', 'Variety name']).size().reset_index(name='Variety Count')

    # Create a bar graph to show the number of varieties available for each crop
    fig = px.bar(variety_count, x='Variety name', y='Variety Count', color='Crops',
                    title='Number of Varieties per Crop',
                    labels={'Variety name': 'Variety', 'Variety Count': 'Count of Varieties'})

    crop_type_distribution = crop_varieties_data.groupby('Type of Crops').size().reset_index(name='Count')

    pie_fig = px.pie(crop_type_distribution, names='Type of Crops', values='Count',
            title='Distribution of Crop Types')
    
    variety_year_count = crop_varieties_data.groupby('Year')['Variety name'].count().reset_index()
    variety_year_count.columns = ['Year', 'Variety Count']

    # Create a bar chart for the number of varieties per year
    bar_fig = px.bar(variety_year_count, x='Year', y='Variety Count',
                title='Number of Varieties Released per Year',
                labels={'Year': 'Year', 'Variety Count': 'Count of Varieties'})
    
    heatmap_data = crop_varieties_data.groupby(['Type of Crops', 'Crops']).size().reset_index(name='Variety Count')

    # Create a heatmap
    heat_fig = px.density_heatmap(heatmap_data, x='Type of Crops', y='Crops', z='Variety Count',
                            title='Heatmap of Crop vs Type of Crop and Variety Count',
                            labels={'Type of Crops': 'Type of Crop', 'Crops': 'Crop', 'Variety Count': 'Count of Varieties'})
        
    return fig,pie_fig,bar_fig,heat_fig
