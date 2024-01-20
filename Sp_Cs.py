import numpy as np
from scipy.spatial import Voronoi, distance

def point_line_distance(point, line_start, line_end):
    return np.abs(np.cross(line_end - line_start, line_start - point)) / np.linalg.norm(line_end - line_start)

def voronoi_distance(points):
    total_params_and_distances_sum = []
    voronoi=Voronoi(points)
    for point in points:
        min_distance = float('inf')
        nearest_edge_params_sum = 0

        for ridge in voronoi.ridge_vertices:
            if ridge[0] != -1 and ridge[1] != -1:
                edge_start = voronoi.vertices[ridge[0]]
                edge_end = voronoi.vertices[ridge[1]]
                dist = point_line_distance(point, edge_start, edge_end)

                if dist < min_distance:
                    min_distance = dist
                    nearest_edge_params_sum = np.linalg.norm(edge_end - edge_start)

        total_params_and_distances_sum.append(nearest_edge_params_sum + min_distance)

        indices = list(range(len(total_params_and_distances_sum)))
        sorted_indices = sorted(indices, key=lambda i: total_params_and_distances_sum[i])

    return sorted_indices

# Przykładowe punkty w przestrzeni 2D.
sample_points = np.array([(2, 3), (5, 8), (8, 4), (9, 7), (12, 5)])

# Obliczanie sumy parametru krzywej Voronoi i odległości od niej dla każdego punktu.
sorted= voronoi_distance(sample_points)
print(sorted)


