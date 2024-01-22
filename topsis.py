from typing import List
import math
import copy


def topsis(data: List[List[float]], lower_limits: List, upper_limits: List, weight_vector: List, benefit_attributes: List)-> List:

    # determining the number of alternatives and criteria
    number_of_alternatives = len(data)
    number_of_criteria = len(data[0]) -1

    # Checking the correctness of sizes
    if all(len(actual_list) == number_of_criteria for actual_list in [lower_limits, upper_limits, weight_vector, benefit_attributes]):

        # Establishing a list of compatible alternatives
        compatible_alternatives = [1 for i in range(number_of_alternatives)]
        compatible_data = []
        compatible_id = []
        for i in range(number_of_alternatives):
            for j in range(0, number_of_criteria):
                if all([data[i][j+1] >= lower_limits[j], data[i][j+1] <= upper_limits[j], compatible_alternatives[i] > 0]):
                    compatible_alternatives[i] = 1
                else:
                    compatible_alternatives[i] = 0
            if compatible_alternatives[i] == 1:
                compatible_data.append(data[i][1:])
                compatible_id.append(data[i][0])

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
                if benefit_attributes[j] == 1:
                    standardized_decision_matrix[i][j] = (1 - compatible_data[i][j] / factor[j]) * weight_vector[j]
                else:
                    standardized_decision_matrix[i][j] = (compatible_data[i][j] / factor[j]) * weight_vector[j]

        # Creating an ideal and anti-ideal vector
        transposed_list = list(zip(*standardized_decision_matrix))
        ideal_vector = [min(column) for column in transposed_list]
        anti_ideal_vector = nadir(copy.deepcopy(standardized_decision_matrix))

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
        for i in range(new_number_of_alternatives):
            scoring_factor.append(distance_from_anti_ideal[i] / (distance_from_ideal[i] + distance_from_anti_ideal[i]))
        merged = list(zip(scoring_factor, compatible_id))
        _, result = zip(*sorted(merged, key=lambda x: x[0], reverse=True))
        result = list(result)
        return result
    else:
        print("Incompatible input data length")


def nadir(X: List[List[float]]) -> List[List[float]]:
    P_X = []
    i = 0
    while i < len(X):
        Y = X[i]
        j = i + 1
        while j < len(X):
            X_j = X[j]
            if all(el1 <= el2 for el1, el2 in zip(Y, X_j)):
                del X[j]
            elif all(el1 <= el2 for el1, el2 in zip(X_j, Y)):
                Y = X_j
                del X[i]
            else:
                j += 1
        if len(P_X) == 0:
            P_X.append(Y)
        else:
            if P_X.count(Y) == 0:
                P_X.append(Y)
        k = 1
        while k < len(X):
            if all(el1 <= el2 for el1, el2 in zip(Y, X[k])):
                del X[k]
            else:
                k += 1
        if Y in X:
            del X[X.index(Y)]
        if len(X) == 1:
            P_X.append(X[0])
            break
    P_X_trans = list(zip(*P_X))
    point_nadir = [max(col) for col in P_X_trans]
    return point_nadir