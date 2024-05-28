# Python code for route optimization using OR-Tools
# Add your route optimization code here

from qgis.core import (QgsVectorLayer, QgsFeature, QgsGeometry, QgsField, QgsProject, QgsPointXY, QgsCoordinateTransform, QgsCoordinateReferenceSystem)
import numpy as np
from scipy.spatial import ConvexHull

# Define the geographical bounds of Kathmandu
min_lat, max_lat = 27.65, 27.75
min_lon, max_lon = 85.27, 85.35

# Generate 200 random nodes within these bounds
num_nodes = 800
np.random.seed(0)
coordinates = np.random.rand(num_nodes, 2)
coordinates[:, 0] = coordinates[:, 0] * (max_lon - min_lon) + min_lon  # Longitude
coordinates[:, 1] = coordinates[:, 1] * (max_lat - min_lat) + min_lat  # Latitude
weights = np.random.rand(num_nodes) * 10  # Random weights between 0 and 10

# Create a new memory layer for points
vl = QgsVectorLayer("Point?crs=EPSG:4326", "KathmanduRandomNodes", "memory")
pr = vl.dataProvider()
pr.addAttributes([QgsField("weight", QVariant.Double)])
vl.updateFields()

# Add points to the layer
for coord, weight in zip(coordinates, weights):
    f = QgsFeature()
    f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(coord[0], coord[1])))
    f.setAttributes([weight])
    pr.addFeature(f)
vl.updateExtents()
QgsProject.instance().addMapLayer(vl)

# Function to divide area into subregions and compute convex hulls
def divide_and_conquer(coords, weights, rows, cols):
    # Define subregion bounds
    lat_range = np.linspace(min_lat, max_lat, rows+1)
    lon_range = np.linspace(min_lon, max_lon, cols+1)
    
    # Create layers for each subregion
    for i in range(rows):
        for j in range(cols):
            # Filter points within subregion
            sub_coords = [coords[k] for k in range(len(coords)) if 
                          lat_range[i] <= coords[k][1] < lat_range[i+1] and 
                          lon_range[j] <= coords[k][0] < lon_range[j+1]]
            if len(sub_coords) >= 3:
                sub_coords = np.array(sub_coords)
                hull = ConvexHull(sub_coords)
                hull_points = [QgsPointXY(sub_coords[v][0], sub_coords[v][1]) for v in hull.vertices]
                hull_poly = QgsGeometry.fromPolygonXY([hull_points])
                
                hull_layer = QgsVectorLayer("Polygon?crs=EPSG:4326", f"ConvexHull_Subregion_{i}_{j}", "memory")
                pr_hull = hull_layer.dataProvider()
                hull_feat = QgsFeature()
                hull_feat.setGeometry(hull_poly)
                pr_hull.addFeature(hull_feat)
                hull_layer.updateExtents()
                QgsProject.instance().addMapLayer(hull_layer)

# Execute the function with desired grid size
divide_and_conquer(coordinates, weights, 10, 10) 
