import numpy as np
import pandas as pd
from numpy.linalg import *
import os
import plotly.graph_objects as go


def list_mult(list1, list2):
    products = []
    for num1, num2 in zip(list1, list2):
        products.append(num1 * num2)
    return np.array(products)

def getPercentageOfChange(values):
    return np.array([values[i]/values[i-1] for i in range(1,len(values))])

def eval_M(M, data, t=0.01):
    change = getPercentageOfChange(data)
    r = np.zeros((3,1)); i = np.zeros((3,1)); good = 0
    for idx, value in enumerate(change[:-1]):
        c = np.zeros((3,1)); p = np.zeros((3,1)); true = np.zeros((3,1))
        if value > 1+t :
            c[0] = 1
        elif value < 1-t :
            c[1] = 1
        else:
            c[2]=1

        if change[idx+1] > 1+t:
            true[0] = 1
        elif change[idx+1] < 1-t:
            true[1] = 1
        else:
            true[2]=1

        p[np.where(M.dot(c) == M.dot(c).max())[0]] = 1
        i += true; 
        if (p-true).T.dot((p-true)).sum() == 0:
            good+=1
            r +=p
    return i, r, good

def get_Markov(data, t=0.01):
    change = getPercentageOfChange(data)

    E = list_mult(sum([(1+t) >= change]), sum([change >= (1-t)]))
    D = sum([(1-t) > change])
    U = sum([change > (1+t)])

    UU = sum([1 if U[i] == 1 and U[i+1] == 1 else 0 for i in range(len(U)-1)]) / sum(U)
    UD = sum([1 if U[i] == 1 and D[i+1] == 1 else 0 for i in range(len(U)-1)]) / sum(U)
    UE = sum([1 if U[i] == 1 and E[i+1] == 1 else 0 for i in range(len(U)-1)]) / sum(U)

    DU = sum([1 if D[i] == 1 and U[i+1] == 1 else 0 for i in range(len(U)-1)]) / sum(D)
    DD = sum([1 if D[i] == 1 and D[i+1] == 1 else 0 for i in range(len(U)-1)]) / sum(D)
    DE = sum([1 if D[i] == 1 and E[i+1] == 1 else 0 for i in range(len(U)-1)]) / sum(D)

    EU = sum([1 if E[i] == 1 and U[i+1] == 1 else 0 for i in range(len(U)-1)]) / sum(E)
    ED = sum([1 if E[i] == 1 and D[i+1] == 1 else 0 for i in range(len(U)-1)]) / sum(E)
    EE = sum([1 if E[i] == 1 and E[i+1] == 1 else 0 for i in range(len(U)-1)]) / sum(E)

    Markov = np.array([[UU, UD, UE], [DU, DD, DE], [EU, ED, EE]], dtype=np.float64)


    return Markov.T
    # print(sum([UU, UD, UE]))
    # print(sum([DU, DD, DE]))
    # print(sum([EU, ED, EE]))

accuracy = [2539, 2441, 2311, 2257, 2122, 1917, 1633, 1553, 1430, 1455, 1492, 1570, 1659, 1760, 1863, 1947, 2046, 2140, 2239, 2344, 2430, 2517, 2594, 2671, 2746, 2839, 2909, 2974, 3031, 3084, 3134, 3195, 3258, 3318, 3372, 3390, 3438, 3442, 3496, 3540, 3583, 3634, 3652, 3686, 3715, 3745, 3768, 3762, 3783, 3805, 3787, 3805, 3832, 3856, 3810, 3827, 3837, 3853, 3859, 3877, 3884, 3898, 3909, 3933, 3938, 3952, 3958, 3830, 3842, 3806, 3768, 3727, 3738, 3748, 3755, 3757, 3719, 3728, 3691, 3564, 3521, 3525, 3526, 3533, 3540, 3542, 3544, 3545, 3502, 3459, 3423, 3431, 3436, 3391, 3396, 3353, 3309, 3309, 3262, 3209, 3162, 3117, 3025, 2888, 2752, 2704, 2562, 2517, 2518, 2475, 2286, 2288, 2155, 2107, 2107, 2013, 2014, 2014, 2015, 1875, 1875, 1827, 1779, 1732, 1654, 1558, 1462, 1414, 1318, 1319, 1318, 1318, 1273, 1225, 1225, 1225, 1226, 1226, 1179, 1179, 1084, 1036, 988, 993, 995, 996, 997, 997, 950, 856, 856, 856, 856, 856, 808, 809, 809, 764, 764, 716, 668, 668, 668, 668, 668, 668, 668, 668, 668, 668, 668, 668, 668, 668, 668, 668, 668, 668, 668, 668, 668, 668, 668, 668, 668, 668, 668, 668, 623, 623, 623, 623, 575, 575, 575, 575, 575, 575, 575, 575, 575, 575, 575, 575, 527, 527, 527, 527, 527, 527, 527, 527, 527, 480, 480, 480, 480, 480, 480, 480, 432, 384, 336, 336, 336, 336, 336, 336, 336, 336, 336, 336, 336, 336, 336, 336]
accuracy = []
UP_accuracy = []
DOWN_accuracy = []
EQUAL_accuracy = []
ts = []
for t in np.arange(0, 0.2, 0.001):
    c = np.zeros((3,1))
    trials = 0; good = 0; total = np.zeros((3,1)); p=np.zeros((3,1))  
    for file in os.listdir("../DATA/training/stocks/"):
        df = pd.read_csv("../DATA/training/stocks/"+file, sep ="|")
        Markov = get_Markov(df.OPEN[:-50], t=t)
        r, i, g = eval_M(Markov, df.OPEN[-50:].values, t=t)
        good+=g; total += i; p +=r
        trials += 50
    ts.append(t)
    print(UP_accuracy)
    print(DOWN_accuracy)
    print(EQUAL_accuracy)
    accuracy.append(good); UP_accuracy.append(p[0]/total[0]); DOWN_accuracy.append(p[1]/total[1]); EQUAL_accuracy.append(p[2]/total[2])
    # print("Evaluation result:")
    # print(c, trials, good)


fig = go.Figure()
fig.add_trace(go.Scatter(x= ts, y= np.array(accuracy)/4800,
                    mode='lines',
                    name='accuracy'))
fig.add_trace(go.Scatter(x= ts, y= UP_accuracy,
                    mode='lines',
                    name='UP'))
fig.add_trace(go.Scatter(x= ts, y= DOWN_accuracy,
                    mode='lines',
                    name='DOWN'))
fig.add_trace(go.Scatter(x= ts, y= EQUAL_accuracy,
                    mode='lines',
                    name='EQUAL'))

fig.show()
print(UP_accuracy)
