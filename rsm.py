import extract_data
import numpy as np
import matplotlib.pyplot as plt
from typing import List
import copy


def is_lower(a, b, benefit_attributes):
    for i in range(len(a)-1):
        if benefit_attributes[i] == 1:
            if a[i+1] > b[i+1]:
                return False
        else:
            if a[i+1] < b[i+1]:
                return False
    return True


def filtration_of_dominated(X, benefit_attributes=None):
    if X.shape[0] == 1:
        return X, []
    if benefit_attributes is None:
        benefit_attributes = np.zeros(len(X))
    
    P = None
    Q = np.zeros([0, X.shape[1]])

    i = 0
    while i < X.shape[0]:
        Y = X[i]

        j = i + 1

        while j < X.shape[0]: 
            if is_lower(Y, X[j], benefit_attributes):
                Q = np.vstack([Q, Y])
                Y = X[j]
                X = np.delete(X, j, 0)
            elif is_lower(X[j], Y, benefit_attributes): 
                #Y = X[j]
                Q = np.vstack([Q, X[j]])
                X = np.delete(X, j, 0)
            else:
                j += 1

        if P is None:
            P = Y
        else:
            P = np.vstack([P, Y])

        k = 0 
        while k < X.shape[0]:
            if is_lower(X[k], Y, benefit_attributes):
                X = np.delete(X, k, 0)
            else:
                k += 1
    return (P, Q)  


def internal_inconsistency(A, benefit_attributes):
    P, _ = filtration_of_dominated(A, benefit_attributes)
    if len(A) == len(P):
        return True
    else:
        return False


def rsm(input_data: List[List[int]], lower_limits: List, upper_limits: List, is_active: List, benefit_attributes: List)-> List:

    # determining the number of criteria
    number_of_criteria = len(input_data[0]) -1
    
    # Checking the correctness of sizes
    if all(len(actual_list) == number_of_criteria for actual_list in [lower_limits, upper_limits, benefit_attributes]):

        input_copy = copy.copy(input_data)

        A0_list = []
        A1_list = []
        i = 0
        while i < len(input_copy):
            for j in range(len(input_copy[0])-1):
                # maximize
                if benefit_attributes[j] == 1:
                    if input_copy[i][j+1] < lower_limits[j]:
                        A1_list.append(input_copy[i])
                        input_copy.pop(i)
                        i-=1
                        break
                    elif input_copy[i][j+1] > upper_limits[j]:
                        A0_list.append(input_copy[i])
                        input_copy.pop(i)
                        i-=1
                        break
                # minimize
                else:
                    if input_copy[i][j+1] > upper_limits[j]:
                        A1_list.append(input_copy[i])
                        input_copy.pop(i)
                        i-=1
                        break
                    elif input_copy[i][j+1] < lower_limits[j]:
                        A0_list.append(input_copy[i])
                        input_copy.pop(i)
                        i-=1
                        break
            i+=1
            
        data = np.array(input_copy)
        A0 = np.array(A0_list)
        A1 = np.array(A1_list)

        if A0.size == 0:
            A0 = np.array([[-1] + [upper_limits[i] if benefit_attributes[i]==1 else lower_limits[i] for i in range(len(benefit_attributes))]])

        if A1.size == 0:
            A1 = np.array([[-1] + [lower_limits[i] if benefit_attributes[i]==1 else upper_limits[i] for i in range(len(benefit_attributes))]])

        for i in range(len(is_active), 0, -1):
            if is_active[i-1] == 0:
                data = np.delete(data, i, axis=1)
                A0 = np.delete(A0, i, axis=1)
                A1 = np.delete(A1, i, axis=1)

        while not internal_inconsistency(A0, benefit_attributes):
            _, A0 = filtration_of_dominated(A0, benefit_attributes)

        while not internal_inconsistency(A1, benefit_attributes):
            A1, _ = filtration_of_dominated(A1, benefit_attributes)

        # print('a0: ', A0)
        # print('a1: ', A1)
        # print('data: ', data)

        P = []
        for i1 in range(A0.shape[0]):
            for j1 in range(A1.shape[0]):
                area = 1
                for idx in range(1, A0.shape[1]):
                    area *= np.abs(A0[i1, idx] - A1[j1, idx])
                P.append(area)

        P = np.array(P)
        w = P / np.sum(P)  

        f = []
        for i in range(data.shape[0]):
            wsp = []
            i_w = 0
            for i1 in range(A0.shape[0]):
                for j1 in range(A1.shape[0]):
                    l = 0
                    m = 0
                    for idx in range(1, A0.shape[1]):
                        l += (A1[j1, idx] - data[i, idx])**2 
                        m += (A0[i1, idx] - data[i, idx])**2 
                    l = np.sqrt(l)
                    m = np.sqrt(m) + l
                    
                    wsp.append(w[i_w] * (l / m))

                    i_w += 1

            f.append(np.concatenate([data[i, :], [np.sum(wsp)]]))

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

    benefit_attributes_ = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    weight_vector_ = []

    transposed_list = list(zip(*r[3]))[1:]
    lower_limits_ = [min(column) for column in transposed_list]
    upper_limits_ = [max(column) for column in transposed_list]

    result_ = rsm(r[3], lower_limits_, upper_limits_, benefit_attributes_, benefit_attributes_)
    print(result_)