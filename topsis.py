from typing import List
import math
import numpy as np

dane = [[700,  2, 6, 8],
        [250,  2, 4, 8],
        [1200, 6, 9, 16],
        [880,  4, 9, 12],
        [450,  3, 8, 12],
        [1900, 8, 10, 18]]


lower_limits_ = [0, 0, 0, 0]
upper_limits_ = [1800, 7, 9, 16]
weight_vector_ = [1/4, 1/4, 1/4, 1/4]
criterion_ = [0, 1, 1, 1]


def topsis(data: List[List[int]], lower_limits: List, upper_limits: List, weight_vector: List, criterion: List):
    # determining the number of alternatives and criteria
    number_of_alternatives = len(data)
    number_of_criteria = len(data[0])

    # Checking the correctness of sizes
    if all(len(actual_list) == number_of_criteria for actual_list in [lower_limits, upper_limits, weight_vector, criterion]):

        # Establishing a list of compatible alternatives
        compatible_alternatives = [1 for i in range(number_of_alternatives)]
        compatible_data = []
        for i in range(number_of_alternatives):
            for j in range(number_of_criteria):
                if all([data[i][j] >= lower_limits[j], data[i][j] <= upper_limits[j], compatible_alternatives[i] > 0]):
                    compatible_alternatives[i] = 1
                else:
                    compatible_alternatives[i] = 0
            if compatible_alternatives[i] == 1:
                compatible_data.append(data[i])

        # Creating a normalized decision matrix taking into account the weight vector
        new_number_of_alternatives = len(compatible_data)
        new_number_of_criteria = len(compatible_data[0])
        standardized_decision_matrix = [[0 for i in range(new_number_of_criteria)] for i in range(new_number_of_alternatives)]
        factor = [0 for i in range(new_number_of_criteria)]
        for j in range(new_number_of_criteria):
            for i in range(new_number_of_alternatives):
                factor[j] += compatible_data[i][j]**2
            factor[j] = math.sqrt(factor[j])
        for j in range(new_number_of_criteria):
            for i in range(new_number_of_alternatives):
                if criterion[j] == 1:
                    standardized_decision_matrix[i][j] = (1 - compatible_data[i][j] / factor[j]) * weight_vector[j]
                else:
                    standardized_decision_matrix[i][j] = (compatible_data[i][j] / factor[j]) * weight_vector[j]

        # Creating an ideal and anti-ideal vector
        transposed_list = list(zip(*standardized_decision_matrix))
        ideal_vector = [min(column) for column in transposed_list]
        anti_ideal_vector = [max(column) for column in transposed_list]

        # Distance calculation
        distance_from_ideal = []
        distance_from_anti_ideal = []
        for i in range(new_number_of_alternatives):
            calculated_sum_ideal = 0
            calculated_sum_anti_ideal = 0
            for j in range(new_number_of_criteria):
                calculated_sum_ideal += (standardized_decision_matrix[i][j] - ideal_vector[j])**2
                calculated_sum_anti_ideal += (standardized_decision_matrix[i][j] - anti_ideal_vector[j]) ** 2
            distance_from_ideal.append(calculated_sum_ideal)
            distance_from_anti_ideal.append(calculated_sum_anti_ideal)

        # Determination of the scoring coefficient
        scoring_factor = []
        for i in range(new_number_of_criteria):
            scoring_factor.append(distance_from_anti_ideal[i] / (distance_from_ideal[i] + distance_from_anti_ideal[i]))
        print("przeszło do końca")
    else:
        print("Incompatible input data length")



if __name__ == "__main__":
    topsis(dane, lower_limits_, upper_limits_, weight_vector_, criterion_)


