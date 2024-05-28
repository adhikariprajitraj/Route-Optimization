import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

# Set seed for reproducibility
np.random.seed(0)

# Generate random nodes
num_nodes = 50
coordinates = np.random.rand(num_nodes, 2) * 100  # Nodes within a 100x100 grid
weights = np.random.rand(num_nodes) * 10  # Weights between 0 and 10

# Set the threshold for selecting nodes
threshold = 5
selected_nodes = coordinates[weights > threshold]

# Check if there are enough nodes to form a convex hull
if len(selected_nodes) >= 3:
    hull = ConvexHull(selected_nodes)
    plt.figure(figsize=(8, 6))
    plt.plot(coordinates[:, 0], coordinates[:, 1], 'o', markersize=5)
    plt.plot(selected_nodes[:, 0], selected_nodes[:, 1], 'o', color='red', label='Selected Nodes')
    for simplex in hull.simplices:
        plt.plot(selected_nodes[simplex, 0], selected_nodes[simplex, 1], 'k-')
    plt.title('Convex Hull of Selected Nodes')
    plt.legend()
    plt.show()
else:
    print("Not enough nodes above the threshold to form a convex hull.")
