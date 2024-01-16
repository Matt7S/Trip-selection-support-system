import extract_data
import numpy as np
import matplotlib.pyplot as plt

def rsm(data, A0, A1, wages=None):
    P = []
    for i1 in range(A0.shape[0]):
        for j1 in range(A1.shape[0]):
            area = 1
            for idx in range(A0.shape[1]):
                area *= np.abs(A0[i1, idx] - A1[j1, idx])
            P.append(area)

    P = np.array(P)
    w = P / np.sum(P)  
    # print("A0: ", A0)
    # print("A1: ", A1)
    # print("P: ", P) 
    # print("w: ", w)

    f = []
    for i in range(data.shape[0]):
        wsp = []
        i_w = 0
        for i1 in range(A0.shape[0]):
            for j1 in range(A1.shape[0]):
                l = 0
                m = 0
                for idx in range(A0.shape[1]):
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
    
    return sorted_data


r = extract_data.get_data_from_database()
arr=np.array(r[3])

A0=np.array([   
    [-2,  0],
    [ 1, -3],
    [ 0, -1]])
A1=np.array([   
    [-1.,  1.],
    [ 3., -1.],
    [ 4., -2.]])
A2=np.array([   
    [ 0.,  1.],
    [-1.,  3.]])

print(rsm(A1, A0, A2))