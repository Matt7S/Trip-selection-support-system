import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

def plot_voronoi(points):
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

# Przykładowe punkty w przestrzeni 2D.
sample_points = [(2, 3), (5, 8), (8, 4), (9, 7), (12, 5)]

# Wywołaj funkcję do rysowania diagramu Voronoi.
plot_voronoi(sample_points)
