
import geopandas as gpd
import matplotlib.pyplot as plt
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

# Load the shapefiles into Geopandas GeoDataFrames
gdfs = [gpd.read_file(os.path.join(current_dir, shapefile)) for shapefile in shapefiles]

# Extract the exterior coordinates of the polygons for plotting
coordinates = []
for gdf in gdfs:
    for geom in gdf.geometry:
        if geom.geom_type == 'Polygon':
            coordinates.append(geom.exterior.coords.xy)

# Plot the extracted coordinates
plt.figure(figsize=(10, 10))
for coord in coordinates:
    plt.plot(coord[0], coord[1], marker='o')

plt.title('Glacier A-81 Movement Over Time')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)
plt.show()
