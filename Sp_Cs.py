import numpy as np
from scipy.spatial import Voronoi, distance, voronoi_plot_2d
import matplotlib.pyplot as plt
from extract_data import get_data_from_database


def spcs_without_idxs_from_db(points):
    """
    Calculate a ranking of points based on their proximity to the nearest edge in a Voronoi diagram and the length of that edge.

    Parameters:
    points (array-like): A list or array of points (e.g., [[x1, y1], [x2, y2], ...]) for which the Voronoi diagram is constructed and analyzed.

    Returns:
    list: A list of indices representing the ranking of the input points. 
    The ranking is determined based on the sum of each point's distance to its nearest Voronoi edge and the length of that edge. A lower sum results in a higher ranking.
    """
    # Initialize a list to store the sum of parameters and distances for each point
    total_params_and_distances_sum = []

    # Create a Voronoi diagram for the given points
    voronoi = Voronoi(points)

    # Iterate over each point to calculate its nearest edge in the Voronoi diagram
    for point in points:
        # Set the initial minimum distance to infinity
        min_distance = float('inf')

        # Initialize the sum of edge parameters (length in this case) for the nearest edge
        nearest_edge_params_sum = 0

        # Iterate over the edges (ridges) of the Voronoi diagram
        for ridge in voronoi.ridge_vertices:
            # Check if the ridge is not a point at infinity
            if np.all(ridge != -1):
                # Get the start and end vertices of the edge
                edge_start = voronoi.vertices[ridge[0]]
                edge_end = voronoi.vertices[ridge[1]]

                # Calculate the distance from the point to this edge
                dist = point_line_distance(point, edge_start, edge_end)

                # Update the minimum distance and nearest edge parameters if this edge is closer
                if dist < min_distance:
                    min_distance = dist
                    nearest_edge_params_sum = np.linalg.norm(edge_end - edge_start)

        # Add the sum of nearest edge parameters and its distance to the list
        total_params_and_distances_sum.append(nearest_edge_params_sum + min_distance)

    # Rank the points based on the sum of parameters and distances
    indices = list(range(len(total_params_and_distances_sum)))
    ranking = sorted(indices, key=lambda i: total_params_and_distances_sum[i])

    return ranking


def plot_voronoi(points):
    """
    Rysuje diagram Voronoi dla zestawu punktów w przestrzeni 2D.

    Parametry:
    points -- lista punktów w formacie [(x1, y1), (x2, y2), ...]
    """
    # Konwertuj punkty na tablicę NumPy.
    points_array = np.array(points)

    # Utwórz obiekt Voronoi dla punktów.
    vor = Voronoi(points_array)

    # Rysuj diagram Voronoi.
    voronoi_plot_2d(vor, show_vertices=False, line_colors='blue', line_width=2, line_alpha=0.6, point_size=5)

    # Rysuj punkty na wykresie.
    plt.scatter(points_array[:, 0], points_array[:, 1], c='red', marker='o')

    # Dodaj etykiety do punktów.
    for i, (x, y) in enumerate(points):
        plt.text(x, y, f'P{i+1}', ha='right', va='bottom', color='black', fontweight='bold')

    # Dodatkowe ustawienia wykresu.
    plt.xlabel('Oś X')
    plt.ylabel('Oś Y')
    plt.title('Diagram Voronoi')
    plt.grid(True)
    plt.show()


def jitter_points(points, jitter_amount=0.01):
    jitter = np.random.normal(scale=jitter_amount, size=points.shape)
    return points + jitter


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


def sp_cs_algorithm(new_test_table):
    """
    Calculate a ranking of points based on their proximity to the nearest edge in a Voronoi diagram and the length of that edge.

    Parameters:
    points (array-like): A list or array of points (e.g., [[idx1, x1, y1, z1], [idx2, x2, y2, z2], ...]) for which the Voronoi diagram is constructed and analyzed.

    Returns:
    list: A list of indices from database representing the ranking of the input points. 
    The ranking is determined based on the sum of each point's distance to its nearest Voronoi edge and the length of that edge. A lower sum results in a higher ranking.
    """
    # Extract the coordinates and database indices
    new_test_table = np.array(new_test_table)
    db_indices = new_test_table[:, 0]
    points = new_test_table[:, 1:]

    # Initialize a list to store the sum of parameters and distances for each point
    total_params_and_distances_sum = []

    # Dodanie niewielkiego szumu do każdego punktu
    jittered_points = jitter_points(points)

    # Create a Voronoi diagram for the given points
    #
    # voronoi = Voronoi(points)
    voronoi = Voronoi(jittered_points)


    # Iterate over each point to calculate its nearest edge in the Voronoi diagram
    for point in points:
        min_distance = float('inf')
        nearest_edge_params_sum = 0

        for ridge in voronoi.ridge_vertices:
            if np.all(ridge != -1):
                edge_start = voronoi.vertices[ridge[0]]
                edge_end = voronoi.vertices[ridge[1]]

                dist = point_line_distance(point, edge_start, edge_end)

                if dist < min_distance:
                    min_distance = dist
                    nearest_edge_params_sum = np.linalg.norm(edge_end - edge_start)

        total_params_and_distances_sum.append(nearest_edge_params_sum + min_distance)

    # Rank the points based on the sum of parameters and distances
    ranking = sorted(range(len(total_params_and_distances_sum)), key=lambda i: total_params_and_distances_sum[i])
    #print(ranking)

    # Return the database indices based on the ranking
    ranked_db_indices = [db_indices[i] for i in ranking]

    return ranked_db_indices


def sp_cs(input_data, lower_limits, upper_limits, criteria_idxs, benefit_attributes):
    # Establishing a list of compatible alternatives
    # determining the number of criteria
    input_data = np.array(input_data)
    data_after_limits = []
    #min_values = np.min(input_data[:,1:], axis=0)
    max_values = np.max(input_data[:,1:], axis=0)


    for row_idx in range(len(input_data)):
        tmp_tab = []
        tmp_tab.append(input_data[row_idx,0])
        for i, cri_idx in enumerate(criteria_idxs):
            if (input_data[row_idx,cri_idx+1] >= lower_limits[i] and input_data[row_idx,cri_idx+1] <= upper_limits[i]):
                if benefit_attributes[cri_idx] == 1:
                    tmp_tab.append(input_data[row_idx,cri_idx+1])
                else:
                    tmp_tab.append(max_values[cri_idx] - input_data[row_idx, cri_idx+1])


            if len(tmp_tab) == 4:
                data_after_limits.append(tmp_tab)
    
    #print(data_after_limits)

    if len(data_after_limits) <= 5:
        return None
    
    ranking = sp_cs_algorithm(data_after_limits)
    return ranking     


def test_spcs_2d():
    # Przykładowe punkty w przestrzeni 2D.
    sample_points = [(2, 3), (5, 5), (8, 4), (9, 7), (12, 5)]

    # Wywołaj funkcję do rysowania diagramu Voronoi.
    plot_voronoi(sample_points)


def test_spcs_3d():
    # Test the modified function
    new_test_table = np.array([[0, 1, 1, 1], [5, 2, 2, 2], [8, 5, 1, 6], [5, 2, 5, 3], [98, 1, 5, 1], [99, 1, 5, 7]])
    modified_ranking = sp_cs_algorithm(new_test_table)
    print(modified_ranking)


def test_with_limits():
    benefit_attributes = [1, 1, 1, 0]
    lower_limits = [2, 2, 2]
    upper_limits = [10, 10, 10]
    cri_idxs = [1, 2, 3]
    data = np.array([[0, 1, 6, 3, 4], [1, 2, 7, 4, 5], [2, 3, 4, 5, 6], [3, 4, 5, 6, 8], [4, 4, 5, 6, 7], [9, 12, 12, 12, 12], [5, 1, 1, 1, 1], [7, 5, 6, 7 ,8]])
    output = sp_cs(data, lower_limits, upper_limits, cri_idxs, benefit_attributes)
    print(output)


def test_with_database():
    r = get_data_from_database()
    benefit_attributes = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    cri_idxs = [2, 3, 4]
    transposed_list = list(zip(*r[3]))[1:]
    minimum = [2,2,2]
    maximum = [10000, 10000, 100]
    output = sp_cs(r[3], minimum, maximum, cri_idxs, benefit_attributes)
    print(output)


if __name__ ==  "__main__":
    #test_spcs_3d()
    #test_with_limits()
    test_with_database()
