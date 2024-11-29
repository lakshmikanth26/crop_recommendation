from flask import Blueprint, render_template, request
import pandas as pd
from .utils.data_processor import process_crop_yield_data, process_crop_price_data, process_rainfall_data, process_crop_variety_data
import plotly.express as px

main_bp = Blueprint('main', __name__)

# Load data
crop_yield_data = pd.read_csv('app/data/crop_yield.csv')
crop_price_data = pd.read_csv('app/data/crop_price.csv')
rainfall_data = pd.read_csv('app/data/India_rainfall.csv')
crop_varieties_data = pd.read_csv('app/data/crop_varieties.csv', encoding='ISO-8859-1')

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/visualize', methods=['POST'])
def visualize():
    analysis_type = request.form['analysis_type']
    
    # Initialize a dictionary to hold graph HTML and headers
    graph_data = {}

    # Handling different analysis types and adding graphs dynamically
    if analysis_type == "crop_yield_vs_rainfall":
        # Process Crop Yield vs Rainfall Data
        fig = process_crop_yield_data(crop_yield_data, rainfall_data)
        graph_data['crop_yield'] = {'header': 'Crop Yield vs Rainfall Analysis', 'graph': fig.to_html(full_html=False)}
    
    elif analysis_type == "crop_price_trends":
        # Process Crop Price Data
        line_fig, box_fig, bar_fig, heatmap_fig = process_crop_price_data(crop_price_data)
        graph_data['crop_price'] = {
            'header': 'Crop Price Trends Over Time',
            'graph': line_fig.to_html(full_html=False),
        }
        graph_data['price_distribution'] = {
            'header': 'Price Distribution per Commodity',
            'graph': box_fig.to_html(full_html=False),
        }
        graph_data['price_comparison'] = {
            'header': 'Commodity Price Comparison by State',
            'graph': bar_fig.to_html(full_html=False),
        }
        graph_data['price_heatmap'] = {
            'header': 'Price Heatmap by State and Commodity',
            'graph': heatmap_fig.to_html(full_html=False),
        }

    elif analysis_type == "rainfall_analysis":
        # Process Rainfall Data - Pass the file path here instead of the DataFrame
        df = process_rainfall_data('app/data/India_rainfall.csv')

        # Plot the data using Plotly (e.g., line plot of Avg_Rainfall)
        fig = px.line(df, x='YEAR', y='Avg_Rainfall', title="Average Rainfall (June - September)", labels={'Avg_Rainfall': 'Average Rainfall (mm)', 'YEAR': 'Year'})
        graph_data['rainfall'] = {'header': 'Rainfall Analysis', 'graph': fig.to_html(full_html=False)}

    elif analysis_type == "crop_varieties":
            # Process Crop Varieties Data
        fig, pie_fig, bar_fig, heat_fig = process_crop_variety_data(crop_varieties_data)
        graph_data['crop_varieties'] = {'header': 'Crop Varieties Distribution', 'graph': fig.to_html(full_html=False)}
        graph_data['pie_chart'] = {'header': 'Crop Varieties Pie Chart', 'graph': pie_fig.to_html(full_html=False)}
        graph_data['variety_count'] = {'header': 'Variety Count per Crop', 'graph': bar_fig.to_html(full_html=False)}
        graph_data['heatmap'] = {'header': 'Variety Heatmap', 'graph': heat_fig.to_html(full_html=False)}

    else:
        graph_data = {}

    return render_template('crop_analysis.html', graph_data=graph_data)
