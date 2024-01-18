from typing import List
import math

def UTA(data: List[List[int]], lower_limits: List, upper_limits: List, weight_vector: List, benefit_attributes: List, num_of_compartments: List)-> List:

    # determining the number of alternatives and criteria
    number_of_alternatives = len(data)
    number_of_criteria = len(data[0])

    # Checking the correctness of sizes
    if all(len(actual_list) == number_of_criteria for actual_list in [lower_limits, upper_limits, weight_vector, benefit_attributes]):

        # Calculating split points
        compartments = []
        weights = []
        for i in range(number_of_criteria):
            step_compartments = (upper_limits[i] - lower_limits[i]) / num_of_compartments[i]
            step_weights = weight_vector[i]/num_of_compartments[i]
            compartments.append([lower_limits[i] + j * step_compartments for j in range(0, num_of_compartments[i]+1)])
            if benefit_attributes[i] == 1:
                weights.append([step_weights*j for j in range(0, num_of_compartments[i] + 1)])
            else:  # min to max
                weights.append([weight_vector[i] - step_weights*j for j in range(0, num_of_compartments[i] + 1)])

        # Assigning weights to split points
        matrix_of_weights = []
        for i in range(number_of_criteria):
            column_of_weights = []
            for j in range(0, num_of_compartments[i]+1):
                if benefit_attributes[i] == 1:
                    value_weight = [compartments[i][j], weights[i][j]]
                else:
                    value_weight = [compartments[i][num_of_compartments[i]-j], weights[i][num_of_compartments[i]-j]]
                column_of_weights.append(value_weight)
            matrix_of_weights.append(column_of_weights)

        # Creation of linear functions parameters
        matrix_of_func_param = []
        for i in range(number_of_criteria):
            compartment_param = []
            for j in range(0, num_of_compartments[i]):
                if j+1 > num_of_compartments[i]:
                    break
                a = (matrix_of_weights[i][j][1] - matrix_of_weights[i][j+1][1])/(matrix_of_weights[i][j][0] - matrix_of_weights[i][j+1][0])
                b = matrix_of_weights[i][j][1] - a * matrix_of_weights[i][j][0]
                compartment_param.append([a,b])
            matrix_of_func_param.append(compartment_param)

        # Creation of scaled matrix
        scaled_data = []
        for i in range(number_of_alternatives):
            scaled_data_col = []
            for j in range(number_of_criteria):
                if benefit_attributes[j] == 1:
                    scaled_data_col.append(min([data[i][j] * matrix_of_func_param[j][k][0] + matrix_of_func_param[j][k][1] for k in range(len(matrix_of_func_param[j]))]))
                else:
                    scaled_data_col.append(max([data[i][j] * matrix_of_func_param[j][k][0] + matrix_of_func_param[j][k][1] for k in range(len(matrix_of_func_param[j]))]))
            scaled_data.append(scaled_data_col)

        # Creation of rank
        rank = [sum(row) for row in scaled_data]
        rank.sort()
        return matrix_of_weights, matrix_of_func_param, scaled_data, rank

if __name__ == "__main__":
    data = [
        [1, 2, 3, 4, 5],
        [2, 3, 4, 5, 6],
        [3, 4, 5, 6, 7],
        [4, 5, 6, 7, 8],
        [5, 6, 7, 8, 9]
    ]
    lower_limits = [1, 2, 3, 4, 5]
    upper_limits = [5, 6, 7, 8, 9]
    weight_vector = [0.2, 0.25, 0.1, 0.05, 0.4]
    benefit_attributes = [1, 0, 1, 0, 1]
    num_of_compartments = [2, 2, 1, 2, 3]

    matrix_of_weights, matrix_of_func_param, scaled_data_col, rank = UTA(data, lower_limits, upper_limits, weight_vector, benefit_attributes, num_of_compartments)
    print(matrix_of_weights, "\n",matrix_of_func_param, "\n",scaled_data_col)

    print(rank)


