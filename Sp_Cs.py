import numpy as np
from scipy.spatial import Voronoi, distance

def point_line_distance(point, line_start, line_end):
    # Oblicz wektor kierunkowy odcinka
    line_direction = line_end - line_start

    # Oblicz wektor od punktu początkowego odcinka do punktu
    vector_to_point = point - line_start

    # Oblicz wektor prostopadły do odcinka i wektora od punktu początkowego odcinka do punktu
    perpendicular_vector = np.cross(line_direction, vector_to_point)

    # Oblicz długość wektora prostopadłego
    perpendicular_distance = np.linalg.norm(perpendicular_vector)

    # Oblicz długość odcinka
    line_length = np.linalg.norm(line_direction)

    # Oblicz odległość punktu od odcinka
    distance = perpendicular_distance / line_length

    return distance
def spcs(points):
    total_params_and_distances_sum = []
    voronoi=Voronoi(points)
    for point in points:
        min_distance = float('inf')
        nearest_edge_params_sum = 0

        for ridge in voronoi.ridge_vertices:
            if np.all(ridge!=-1):
                edge_start = voronoi.vertices[ridge[0]]
                edge_end = voronoi.vertices[ridge[1]]
                dist = point_line_distance(point, edge_start, edge_end)

                if dist < min_distance:
                    min_distance = dist
                    nearest_edge_params_sum = np.linalg.norm(edge_end - edge_start)

        total_params_and_distances_sum.append(nearest_edge_params_sum + min_distance)

        indices = list(range(len(total_params_and_distances_sum)))
        ranking = sorted(indices, key=lambda i: total_params_and_distances_sum[i])

    return ranking



