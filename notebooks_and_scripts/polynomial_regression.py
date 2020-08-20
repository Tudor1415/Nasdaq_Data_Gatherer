import numpy as np 
import plotly.graph_objects as go
import pandas as pd


df = pd.read_csv("../DATA/training/stocks/AAPL.csv", sep ="|")

# def gaussian_elimination(A, b):
#     # Conmputing the LU factorisation
#     E = np.identity(A.shape[0]); x = np.zeros(A.shape[1])
#     for _ in range(A.shape[0]):
#         for i in range(A.shape[1]):
#             E_t = np.identity(A.shape[0])
#             for j in range(i+1, A.shape[0]):
#                 E_t[j][i] = -(A[j][i]/A[i][i])
#             E = E_t.dot(E)

#     U = E.dot(A)
#     b = E.dot(b)
#     print(U)
#     # # Doing backsubstitution
#     # for i in reversed(range(A.shape[1])):
#     #     for j in reversed(range(, A.shape[0])):
#     #         x[i] = b[i]/U[j][i]
#     #         x[i] = b[i]/U[j][i] - x[i-1] 



# gaussian_elimination(np.random.randint(1,10, size=(5, 3)), np.random.randint(1,10, size=(5, 1)))

def get_power_matrix(days, n):
    array = np.ones((days.shape[0], n))
    for i in range(days.shape[0]):
        for j in range(1,n):
           array[i][j] = days[i]**j
    return array

def ploynomial(w, x):
    y = 0
    for p, c in enumerate(w[0]):
        y += c*np.power(x, p)
    return y

def optimize(n):
    mse = []
    # we test for multiple degrees of polynomials
    for d in n:
        p_m = get_power_matrix(np.arange(0,150), d) # geets a power matrix with 100 rows and d as columns 
        w = np.linalg.lstsq(p_m, df["OPEN"].values[-200:-50])
        preds = [ploynomial(w, x) for x in range(150)]
        mse.append(sum([(preds[idx]-i)**2 for idx, i in enumerate(df["OPEN"].values[-50:])])/150)
    print(mse)
    return mse.index(min(mse))

options = np.arange(7,25)
best = optimize(options)
print(best)
p_m = get_power_matrix(np.arange(0,150), options[best])
w = np.linalg.lstsq(p_m, df["OPEN"].values[-200:-50])
preds = [i for i in df["OPEN"].values[:-50]] + [ploynomial(w, x) for x in range(350)]

fig = go.Figure()
fig.add_trace(go.Scatter(x= df["Unnamed: 0"], y= df["OPEN"],
                    mode='lines',
                    name='lines'))
fig.add_trace(go.Scatter(x= df["Unnamed: 0"], y=preds,
                    mode='lines',
                    name='lines'))

fig.show()