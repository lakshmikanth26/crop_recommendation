import plotly.express as px

def plot_prediction(data, crop, year):
    # Check if the filtered data is valid
    print(f"Data passed to plot: {data}")  # Check if data is valid and not empty

    if data.empty:
        return None 

    fig = px.bar(
        data,
        x='State',  # Ensure 'State' column exists in your filtered data
        y='Yield',  # Ensure 'Yield' column exists in your filtered data
        color='Yield',  # Optional: Change this if needed
        title=f"Yield Prediction for {crop} in {year}",
        labels={'Yield': 'Yield (tons/hectare)', 'State': 'State'}
    )
    
    # Save the plot as an HTML file
    fig.write_html("app/templates/plot.html")
    
    return "plot.html"
