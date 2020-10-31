import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
import pandas as pd
from sklearn.feature_selection import chi2

# def ma(data, n):
#     return [sum(data[i: i+n]) / n if i != None  else 0 for i in range(len(data)-n) ]
    
# def diff(data, n):
#     [data[i+1]/data[i] for i in range(len(data)-1) ]

# df = pd.read_csv("../DATA/training/stocks/AAPL.csv", sep ="|")   
# X_train = []; y_train = []
# X_test = []; y_test = []

# for i in range(700):
#     X_train.append(df["OPEN"][i:i+50])
#     y_train.append(df["OPEN"][i+50])

# for i in range(700, 900):
#     X_test.append(df["OPEN"][i:i+50])
#     y_test.append(df["OPEN"][i+50])

# poly = PolynomialFeatures(interaction_only=True)
# f = poly.fit_transform(X_train)

# pol_reg = LinearRegression()
# pol_reg.fit(f, y_train)

# preds = np.concatenate([np.array([0 for _ in range(760)]), pol_reg.predict(poly.fit_transform(X_test))])
# fig = go.Figure()
# fig.add_trace(go.Scatter(x= df["Unnamed: 0"], y= df["OPEN"],
#                     mode='lines+markers',
#                     name='stock'))
# fig.add_trace(go.Scatter(x= df["Unnamed: 0"], y=preds,
#                     mode='lines',
#                     name='predictions'))
# fig.add_trace(go.Scatter(x= df["Unnamed: 0"], y=ma(preds,7),
#                     mode='lines',
#                     name='ma_preds_7'))
# fig.add_trace(go.Scatter(x= df["Unnamed: 0"], y=ma(preds,14),
#                     mode='lines',
#                     name='ma_preds_14'))
# fig.add_trace(go.Scatter(x= df["Unnamed: 0"], y=np.diff(df["OPEN"],1),
#                     mode='lines',
#                     name='stock_diff'))
# fig.add_trace(go.Scatter(x= df["Unnamed: 0"], y=np.diff(preds,1),
#                     mode='lines',
#                     name='preds_diff'))
# fig.add_trace(go.Scatter(x= df["Unnamed: 0"], y=np.diff(ma(preds,14),1),
#                     mode='lines',
#                     name='ma_preds_14_diff'))
        
# fig.show()

# print(np.square(np.diff(ma(preds[750:],14),1) - np.diff(df["OPEN"][750:936],1)).mean(axis=0))
# print(np.square(preds[750:] - df["OPEN"][750:950]).mean(axis=0))

# trials = np.random.randint(1,4, size=(1,1_000_000))[0]

# OO = sum([trials == 1]  and [trials == 1]).sum() / len(trials)
# OT = sum([trials == 1]  and [trials == 2]).sum() / len(trials)
# OTh = sum([trials == 1] and [trials == 3]).sum() / len(trials) 

# TO = sum([trials == 2]  and [trials == 1]).sum() / len(trials)
# TT = sum([trials == 2]  and [trials == 2]).sum() / len(trials) 
# TTh = sum([trials == 2] and [trials == 3]).sum() / len(trials) 

# ThO = sum([trials == 3]   and [trials == 1]).sum() / len(trials) 
# ThT = sum([trials == 3]   and [trials == 2]).sum() / len(trials) 
# ThTh = sum([trials == 3]  and [trials == 3]).sum() / len(trials) 

# Markov = np.array([[OO, OT, OTh], [TO, TT, TTh], [ThO, ThT, ThTh]], dtype=np.float64)

# print(Markov)