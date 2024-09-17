import os
import pandas as pd
import plotly.express as px
from datetime import datetime

# Define the directory where the CSV files are stored
data_dir = 'Data'

# Initialize an empty list to store the filtered data
filtered_data = []

# Loop through all the CSV files in the 'Data' folder
for filename in os.listdir(data_dir):
    if filename.endswith('.csv'):
        # Extract the date from the filename by slicing the last 12 characters and removing the .csv extension
        date_str = filename[-12:-4]  # Extract 'DDMMYYYY' from 'AntarcticIcebergs_DDMMYYYY.csv'

        # Parse the date in the correct format (DDMMYYYY)
        try:
            date = datetime.strptime(date_str, '%d%m%Y')
        except ValueError as e:
            print(f"Error parsing date for file: {filename}, error: {e}")
            continue

        # Load the CSV file
        file_path = os.path.join(data_dir, filename)
        df = pd.read_csv(file_path)

        # Filter for rows where 'Iceberg' is A-81
        df_a81 = df[df['Iceberg'] == 'A81'].reset_index(drop=True)

        # Check if the DataFrame is not empty before assigning the date
        if not df_a81.empty:
            # Add the date information to the DataFrame
            df_a81.loc[:, 'Date'] = date

            # Append the filtered data to the list
            filtered_data.append(df_a81)

# Concatenate all filtered DataFrames into one
df_a81_all = pd.concat(filtered_data, ignore_index=True)

# Sort the DataFrame by the 'Date' column
df_a81_all = df_a81_all.sort_values(by='Date')

# Create a scatter plot using plotly to visualize the glacier's movement over time
fig = px.scatter_geo(df_a81_all,
                     lon='Longitude',
                     lat='Latitude',
                     animation_frame='Date',
                     title="Glacier A-81 Movement Over Time",
                     projection="stereographic")

# Customize the map
fig.update_traces(marker=dict(size=5, opacity=0.7), selector=dict(mode='markers'))

# Adjust the projection scale and center the map on Antarctica
fig.update_layout(
    geo=dict(
        showland=True,
        showcountries=False,
        landcolor="lightgray",
        showocean=True,
        oceancolor="lightblue",
        projection_scale=2,
        center=dict(lat=-75, lon=-45),  # Center the map on Weddell Bay
        projection_type="stereographic"
    )
)

# Show the plot
fig.show()
