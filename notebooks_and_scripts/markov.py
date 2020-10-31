import numpy as np
import pandas as pd
from numpy.linalg import *
import os
import plotly.graph_objects as go
import tensorflow as tf

def get_acc(true, data):
    acc = np.zeros_like(data)
    print(acc.shape)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            print(acc[i][j])
            print(data[i][j])
            print(true[i][j])
            acc[i][j] = data[i][j] / true[i][j][0]
    return acc

def list_mult(list1, list2):
    products = []
    for num1, num2 in zip(list1, list2):
        products.append(num1 * num2)
    return np.array(products)

def getPercentageOfChange(values):
    return np.array([values[i]/values[i-1] for i in range(1,len(values))])

def predict(M, data, t=0.01):
    change = getPercentageOfChange(data); preds = []; true_v = []
    for idx, value in enumerate(change[:-1]):
        c = np.zeros((3,1)); p = np.zeros((3,1)); true = np.zeros((3,1))
        if value > 1+t :
            c[0] = 1
        elif value < 1-t :
            c[1] = 1
        else:
            c[2]=1
        if change[idx+1] > 1+t :
            true[0] = 1
        elif change[idx+1] < 1-t :
            true[1] = 1
        else:
            true[2]=1
        # p[np.where(M.dot(c) == M.dot(c).max())[0]] = 1
        true_v.append(true)
        P_final = M.dot(c)
        P_final[np.where(P_final==np.max(P_final))] = 1
        P_final[np.where(P_final!=np.max(P_final))] = 0
        preds.append(P_final)  
        
    return preds, true_v

def predict_one(M, value, t):
    c = np.zeros((3,1))
    if value > 1+t :
        c[0] = 1
    elif value < 1-t :
        c[1] = 1
    else:
        c[2]=1
    P_final = M.dot(c)
    P_final[np.where(P_final==np.max(P_final))] = 1
    P_final[np.where(P_final!=np.max(P_final))] = 0
    if P_final[0] == 1:
        return 1
    elif P_final[1] == 1:
        return -1
    else:
        return 0


def get_Markov(data, t=0.01):
    try:
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
    except:
        return np.ones((3,3))

def get_variance_in_30_d(data, test):
    variance = []
    ME1 = get_Markov(data, t=0.008)
    ME2 = get_Markov(data, t=0.082)
    # MU1 = get_Markov(data, t=0.018)
    for i in test:
        v = 1
        for p in range(30):
            ME1_p = np.linalg.matrix_power(ME1, p)
            ME2_p = np.linalg.matrix_power(ME2, p)
            v += predict_one(ME2_p, i, t=0.082) + predict_one(ME1_p, i, t=0.008)
        variance.append(v)
    return variance

def get_random_pred(shape):
 
    return p

acc_h =  []; all_true = np.zeros((3, 48)); all_pred = np.zeros((3, 48)); random = np.zeros((10,3, 48))
acc_r = []; ts=[]; count = 0
for t in np.arange(0, 0.015, 0.001):
    for file in os.listdir("../DATA/training/stocks/"):
        df = pd.read_csv("../DATA/training/stocks/"+file, sep ="|")
        if df.OPEN.shape[0] > 700:
            Markov = get_Markov(df.OPEN[:-150], t=t)
            preds, true = predict(Markov, df.OPEN[-150:-100].values, t=t)
            all_true=np.add(all_true , np.hstack(true)); all_pred=np.add(all_pred , np.hstack(preds))
            for i in range(10):
                p = np.random.randint(1,30,size=(3,48))
                for j in range(p.shape[1]):
                    p.T[i][np.where(p.T[i]==np.max(p.T[i]))] = 1
                    p.T[i][np.where(p.T[i]!=np.max(p.T[i]))] = 0
                p[np.where(p>0)] = 1
                random[i] = np.add(p, random[i])
        else:
            pass
    print(t)
    acc = np.divide(all_pred.sum(axis=1).T, all_true.sum(axis=1).T)
    acc_h.append(acc)
    ts.append(t)

acc_h = np.vstack(acc_h)

for i in range(10):
    random[i] = np.divide(random[i], all_true)

fig = go.Figure()

fig.add_trace(go.Scatter(x= ts, y= acc_h.T[0],
                    mode='lines',
                    name='accuracy_UP'))
fig.add_trace(go.Scatter(x= ts, y= acc_h.T[1],
                    mode='lines',
                    name='accuracy_DOWN'))
fig.add_trace(go.Scatter(x= ts, y= acc_h.T[2],
                    mode='lines',
                    name='accuracy_EQUAL'))
for i in range(10):
    fig.add_trace(go.Scatter(x= ts, y= random[i][0],
                    mode='lines',
                    name='accuracy_random_UP'))
    fig.add_trace(go.Scatter(x= ts, y= random[i][1],
                    mode='lines',
                    name='accuracy_random_DOWN'))
    fig.add_trace(go.Scatter(x= ts, y= random[i][2],
                    mode='lines',
                    name='accuracy_random_EQUAL'))

fig.show()


