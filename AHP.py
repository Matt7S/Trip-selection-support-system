import extract_data
import numpy as np
import matplotlib.pyplot as plt
from typing import List
import copy

def ahp(input_data: List[List[int]], lower_limits: List, upper_limits: List, criteria_idxs: List, criteria_comparison: List, benefit_attributes: List)-> List:

    # determining the number of criteria
    number_of_criteria = len(lower_limits)
    
    # Checking the correctness of sizes
    if all(len(actual_list) == number_of_criteria for actual_list in [lower_limits, upper_limits, criteria_idxs]):

        # Cutting unnecessary criteria
        input_copy = copy.copy(input_data)
        input_copy = [[row[i+1] for i in criteria_idxs] for row in input_copy]
        input_copy = [[idx] + row for idx, row in enumerate(input_copy)]

        benefit_attributes_copy = copy.copy(benefit_attributes)
        benefit_attributes_copy = [benefit_attributes_copy[i] for i in criteria_idxs]

        # Cutting alternatives outside the accepted parameters
        i = 0
        while i < len(input_copy):
            for j in range(len(input_copy[0])-1):
                # maximize
                if benefit_attributes[j] == 1:
                    if input_copy[i][j+1] < lower_limits[j]:
                        input_copy.pop(i)
                        i-=1
                        break
                    elif input_copy[i][j+1] > upper_limits[j]:
                        input_copy.pop(i)
                        i-=1
                        break
                # minimize
                else:
                    if input_copy[i][j+1] > upper_limits[j]:
                        input_copy.pop(i)
                        i-=1
                        break
                    elif input_copy[i][j+1] < lower_limits[j]:
                        input_copy.pop(i)
                        i-=1
                        break
            i+=1
            
        data = np.array(input_copy)

        # Creating matrix A - preferences matrix
        dim = len(criteria_idxs)
        A = np.eye(dim)
        idx = 0
        for i in range(1, dim):
            for j in range(dim-1, i-1, -1):
                A[i-1][j] = criteria_comparison[idx]
                A[j][i-1] = 1/criteria_comparison[idx]
                idx += 1

        # Calculating matrix B - normalized preferences matrix
        B = np.zeros([dim, dim])
        for i in range(A.shape[0]):
            for j in range(A.shape[1]):
                B[i][j] = A[i][j] / np.sum(A[:, j])

        # Calculating vector w - criteria weights
        w = np.zeros(dim)
        for i in range(dim):
            w[i] = 1/dim * np.sum(B[i, :])

        Aw = np.dot(A, w)

        # Calculating gamma - maximum eigenvalue of a matrix   
        gamma = 0
        for i in range(dim):
            gamma += Aw[i]/w[i]
        gamma /= dim

        # Calculating CI - consistency index
        CI = (gamma-dim)/(dim - 1)

        # Calculating CR - consistency index
        r = [0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
        CR = CI/r[dim-2]

        # Check if criteria are consistent (CR less than 10%)
        if (CR > 10):
            return None

        # alternative vector weight
        v = np.zeros([dim, data.shape[0]])

        for crit_idx in range(1, dim+1):
            # Creating alternative matrix
            A_A = np.eye(data.shape[0])
            for i in range(1, A_A.shape[0]):
                for j in range(i, A_A.shape[1]):
                    if benefit_attributes_copy[crit_idx-1] == 0:
                        A_A[i-1][j] = data[i-1][crit_idx]/data[j][crit_idx]
                        A_A[j][i-1] = data[j][crit_idx]/data[i-1][crit_idx]
                    else:
                        A_A[j][i-1] = data[i-1][crit_idx]/data[j][crit_idx]
                        A_A[i-1][j] = data[j][crit_idx]/data[i-1][crit_idx]

            # Calculating normalized A_A
            A_B = np.zeros([data.shape[0], data.shape[0]])
            for i in range(A_A.shape[0]):
                for j in range(A_A.shape[1]):
                    A_B[i][j] = A_A[i][j] / np.sum(A_A[:, j])

            # Calculating v - alternative vector weight
            for i in range(v.shape[0]):
                v[i][crit_idx] = 1/v.shape[1] * np.sum(A_B[i, :])

        f = []
        for i in range(data.shape[0]):
            # Calculating final weights
            weight = [w[j]*v[j][i] for j in range(dim)]
            f.append(np.concatenate([data[i, :], [np.sum(weight)]]))
        
        f = np.array(f)

        sorted_indices = np.argsort(f[:, -1])
        sorted_data = f[sorted_indices]

        first_column = sorted_data[:, 0]
        first_column = [int(i) for i in first_column]

        return first_column

    else:
        print("Incompatible input data length")


if __name__ == "__main__":
    r = extract_data.get_data_from_database()

    transposed_list = list(zip(*r[3]))[1:]
    lower_limits_ = [10.0, 50.0, 50.0, 40.0, 0.0]
    upper_limits_ = [2000.0, 95.0, 90.0, 99.0, 11000.0]
    criteria_idxs = [1, 3, 5, 9, 2]
    criteria_comparison = [1, 6, 7, 7, 0.3333333333333333, 7, 0.3333333333333333, 0.14285714285714285, 6, 2]
    benefit_attributes_ = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    result_ = ahp(r[3], lower_limits_, upper_limits_, criteria_idxs, criteria_comparison, benefit_attributes_)
    print(result_)