from typing import List
import extract_data
import numpy as np

def UTA_star(data: List[List[int]], lower_limits: List, upper_limits: List, weight_vector: List, benefit_attributes: List, num_of_compartments: List)-> List:

    # determining the number of alternatives and criteria
    number_of_alternatives = len(data)
    number_of_criteria = len(data[0])-1
    if any(el <= 0 for el in num_of_compartments):
        return 1

    # Checking the correctness of sizes
    if all(len(actual_list) == number_of_criteria for actual_list in [lower_limits, upper_limits, weight_vector, benefit_attributes,num_of_compartments]):

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
                for k in range(len(compartments[j])-1):
                    val = data[i][j + 1]
                    comp = compartments[j][k]
                    if val >= comp and val < compartments[j][k+1]:
                        scaled_data_col.append(val * matrix_of_func_param[j][k][0] + matrix_of_func_param[j][k][1])
            scaled_data.append(scaled_data_col)

        # Creation of rank
        rank = [sum(row) for row in scaled_data]
        sorted_indexes = np.argsort(rank).tolist()
        return sorted_indexes
    else:
        print("Incompatible input data length")
if __name__ == "__main__":

    r = extract_data.get_data_from_database()

    benefit_attributes_ = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    weight_vector_ = [0.833,0.833,0.833,0.833,0.833,0.833,0.833,0.833,0.833,0.833,0.833,0.833,0.833]
    num_of_compartments = [3,2,2,4,1,1,3,2,1,1,1,2,1]
    transposed_list = list(zip(*r[3]))[1:]
    lower_limits_ = [min(column) for column in transposed_list]
    upper_limits_ = [max(column) for column in transposed_list]
    rank = UTA_star(r[3], lower_limits_, upper_limits_, weight_vector_, benefit_attributes_,num_of_compartments)
    print(rank)


