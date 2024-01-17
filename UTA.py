from typing import List
import math

def UTA(data: List[List[int]], lower_limits: List, upper_limits: List, weight_vector: List, benefit_attributes: List, num_of_compartments: List)-> List:


    # determining the number of alternatives and criteria
    number_of_alternatives = len(data)
    number_of_criteria = len(data[0])

    # Checking the correctness of sizes
    if all(len(actual_list) == number_of_criteria for actual_list in [lower_limits, upper_limits, weight_vector, benefit_attributes]):

        # Obliczanie punktów podziału
        compartments = []
        weights = []
        for i in range(len(data[0])):
            step_compartments = (upper_limits[i] - lower_limits[i]) / num_of_compartments[i]
            step_weights = weight_vector[i]/num_of_compartments[i]
            compartments.append([lower_limits[i] + j * step_compartments for j in range(0, num_of_compartments[i]+1)])
            if benefit_attributes[i] == 1:
                weights.append([step_weights*j for j in range(0, num_of_compartments[i] + 1)])
            else:  # min to max
                weights.append([weight_vector[i] - step_weights*j for j in range(0, num_of_compartments[i] + 1)])


        matrix_of_weights = []
        # Przypisywanie wag do punktów podziału
        for i in range(len(data[0])):
            column_of_weights = []
            for j in range(0, num_of_compartments[i]+1):
                if benefit_attributes[i] == 1:
                    value_weight = {compartments[i][j]: weights[i][j]}
                else:
                    value_weight = {compartments[i][num_of_compartments[i]-j]: weights[i][num_of_compartments[i]-j]}
                column_of_weights.append(value_weight)
            matrix_of_weights.append(column_of_weights)
        return matrix_of_weights




