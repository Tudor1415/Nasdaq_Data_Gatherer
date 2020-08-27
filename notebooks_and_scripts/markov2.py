import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

def get_P(DAY, data):
    P_zero = np.zeros((10,1))
    for idx, i in enumerate(range(-25,25,5)):
        if data[:,2][DAY] >  data[:,2][DAY+1]*i/100 and data[:,2][DAY] < data[:,2][DAY+1]*(i+5)/100:
            P_zero[idx] = 1
    return P_zero

def getProbabilities(data, DAY, preds=1, plot=False):
    prob = []
    for i in range(-25,25,5):
        prob_v = []
        for idx, v in enumerate(data[:,-2][:DAY]):
            if v >  data[:,2][idx+1]*i/100 and v < data[:,2][idx+1]*(i+5)/100:
                # print(v, data[:,2][idx]*i/100 , data[:,2][idx]*(i+5)/100, i)
                prob_v.append(abs(v))

        prob.append(sum(prob_v) / data[:,:DAY].shape[0])
    if plot:
        print(sum(prob))
        plt.bar( range(-100,100,5), prob)
        plt.show()

    Markov = np.array(prob).reshape(10,1).dot(np.array(prob).reshape(1,10))
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

# data_t = data[0][1].values
# getProbabilities(data_t, 1000)
_ = plt.hist( data[0][1]["diff1"], bins=np.arange(-6, 6)) 
plt.show()
print("Done")
error = 0
for DAY in range(1000, 1500):
    for name, df in data:
        P_final = getProbabilities(df.values, DAY)
        P_true = get_P(DAY+30, df.values)
        P_final[np.where(P_final==np.max(P_final))] = 1
        P_final[np.where(P_final!=np.max(P_final))] = 0
        error += (P_true - P_final).T.dot((P_true - P_final))
        print(f"For {name} the probability is: \n{P_final} and {P_true}")

    print(f"Day={DAY}, error={error}")
