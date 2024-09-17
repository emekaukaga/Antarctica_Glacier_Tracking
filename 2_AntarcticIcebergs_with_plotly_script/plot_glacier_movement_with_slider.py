
import geopandas as gpd
import plotly.express as px
import pandas as pd
import os

# Define the current directory where the shapefiles are located
current_dir = os.path.dirname(__file__)

# List of shapefiles to be loaded (within the same folder)
shapefiles = [
    'Icebergs_20240419.shp',
    'Icebergs_20240426.shp',
    'Icebergs_20240502.shp',
    'Icebergs_20240509.shp',
    'Icebergs_20240517.shp'
]

# Corresponding dates for the shapefiles
dates = [
    '2024-04-19', 
    '2024-04-26', 
    '2024-05-02', 
    '2024-05-09', 
    '2024-05-17'
]

# Load the shapefiles into GeoDataFrames and extract the coordinates
data = []
for shapefile, date in zip(shapefiles, dates):
    gdf = gpd.read_file(os.path.join(current_dir, shapefile))

    # Add this line to reproject to WGS84 (longitude and latitude)

    gdf = gdf.to_crs(epsg=4326)
    for geom in gdf.geometry:
        if geom.geom_type == 'Polygon':
            coords = list(geom.exterior.coords)
            for coord in coords:
                lon, lat = coord
                data.append({'Date': date, 'Longitude': lon, 'Latitude': lat})

# Convert to a pandas DataFrame
df = pd.DataFrame(data)

# Create a Plotly Express scatter mapbox for the glacier's movement
fig = px.scatter_geo(df,
                     lon='Longitude',
                     lat='Latitude',
                     animation_frame='Date',
                     title="Glacier A-81 Movement Over Time",
                     projection="stereographic")

# Customize the animation and styling
fig.update_traces(marker=dict(size=10, opacity=0.7),
                  selector=dict(mode='markers'))

# Add date slider and play/pause button
fig.update_layout(
    geo=dict(
        showland=True,
        showcountries=True,
        landcolor="lightgray",
        showocean=True,
        oceancolor="lightblue",
        projection_scale=1.5,  # Adjust to focus on Antarctica # Adjusted scale to zoom out
        #center=dict(lat=-90, lon=0)  # Center the map on Antarctica
    ),
    updatemenus=[{
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}],
                "label": "Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top"
    }],
    sliders=[{
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Date: ",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": [
            {"args": [
                [date], {"frame": {"duration": 300, "redraw": True},
                         "mode": "immediate",
                         "transition": {"duration": 300}}
             ],
             "label": date,
             "method": "animate"} for date in dates]
    }]
)

# Show the plot
fig.show()
