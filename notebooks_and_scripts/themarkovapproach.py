import numpy as np
import pandas as pd
import os

def get_P(DAY, data):
    P_zero = np.zeros((3,1))
    if data["diff1"].iloc[DAY] > 0:
        P_zero[0] = 1
    elif data["diff1"].iloc[DAY] < 0:
        P_zero[1] = 1
    else:
        P_zero[2] = 1
    return P_zero

def getProbabilities(data, DAY, preds = 1):
    CC = sum([data["diff1"][:DAY]>0] and [data["diff2"][:DAY]>0]).sum() / data[:DAY].shape[0]
    SS = sum([data["diff1"][:DAY]<0] and [data["diff2"][:DAY]<0]).sum() / data[:DAY].shape[0]
    EE = sum([data["diff1"][:DAY] == 0] and [data["diff2"][:DAY] == 0]).sum() / data[:DAY].shape[0]
    CS = sum([data["diff1"][:DAY]>0] and [data["diff2"][:DAY]<0]).sum() / data[:DAY].shape[0]
    CE = sum([data["diff1"][:DAY]>0] and [data["diff2"][:DAY]==0]).sum() / data[:DAY].shape[0]
    SC = sum([data["diff1"][:DAY]<0] and [data["diff2"][:DAY]>0]).sum() / data[:DAY].shape[0]
    SE = sum([data["diff1"][:DAY]<0] and [data["diff2"][:DAY]==0]).sum() / data[:DAY].shape[0]
    ES = sum([data["diff1"][:DAY] == 0] and [data["diff2"][:DAY] < 0]).sum() / data[:DAY].shape[0]
    EC = sum([data["diff1"][:DAY] == 0] and [data["diff2"][:DAY] > 0]).sum() / data[:DAY].shape[0]

    Markov = np.array([[CC,SC,EC], [CS,SS,ES], [CE,SE,EE]])
    P_zero = get_P(DAY, data)
    Markov = np.linalg.matrix_power(Markov, preds)
    P_final = Markov.dot(P_zero)
    return P_final

data = [(i,pd.read_csv(f"../DATA/historical_prices/{i}", sep ="|")) for i in os.listdir("../DATA/historical_prices/")[1:25]]

for name, df in data:
    shift = df["OPEN"].shift(1)
    df["diff1"] =  df["OPEN"] - shift

    df["diff2"] =  df["diff1"].shift(-1)
    # df["diff3"] =  df["diff2"].shift(-1)

    df.dropna(inplace=True)

# error = 0
# for DAY in range(1000, 1500):
#     for name, df in data:
#         P_final = getProbabilities(df, DAY)
#         P_true = get_P(DAY+30, df)
#         P_final[np.where(P_final==np.max(P_final))] = 1
#         P_final[np.where(P_final!=np.max(P_final))] = 0
#         error += (P_true - P_final).T.dot((P_true - P_final))
#         # print(f"For {name} the probability is: \n{P_final} and {P_true}")

#     print(f"Day={DAY}, error={error}")

# Simulation:
# BALANCE = 250000
# ASSETS = []
# for DAY in range(1000, 1500):
#     rising = []
#     for name, df in data:
#         P_final = getProbabilities(df, DAY)
#         rising.append((name,P_final))


#     if BALANCE > 0:
#         rising.sort(key=lambda x: x[1][0])
#         for i in rising[:5]:
#             for name , df in data:
#                 if name == i[0]:
#                     assets = (BALANCE*0.2) % df.OPEN[DAY]
#                     BALANCE -= assets * df.OPEN[DAY]
#                     ASSETS.append([name, assets, df])

#     if len(ASSETS) > 0:
#         for idx, (name_a, q, df) in enumerate(ASSETS):
#             for name_p, prob in rising:
#                 if name_p == name_a and prob[0] < prob[1]:
#                     BALANCE += q*df.OPEN[DAY+1]
#                     ASSETS.pop(idx) 
    
# print(BALANCE)
                    
        

