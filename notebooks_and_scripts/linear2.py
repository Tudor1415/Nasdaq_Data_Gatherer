import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
data = pd.read_csv("../DATA/training/stocks/AAPL.csv", sep ="|")
target = data["OPEN"].shift(-30)
data.dropna(inplace=True)

data.drop("Unnamed: 0", axis=1,inplace=True)
data.drop("TargetProbability", axis=1,inplace=True)
data.drop("prctChangeOPEN", axis=1,inplace=True)
data.drop("OPEN", axis=1,inplace=True)
data = data.replace([np.inf, -np.inf], np.nan)
data.dropna(inplace=True)

print(data.replace)


IN, IN_test, OUT, OUT_test = train_test_split(data, target, test_size=0.2, random_state=42)

print("Started fitting")
# Turing A and b into square matrix
A = np.array(IN).T.dot(IN)
b = np.array(IN).T.dot(OUT)
# Solving the system 
x = np.linalg.lstsq(A,b)[0]
print("Done!")

preds = np.array(IN_test).dot(x)
mse = np.square(preds - OUT_test).mean(axis=0)
print(preds.shape)
for i in np.random.randint(0,350, size=(20,1)):
    print(f"True value: {np.array(OUT_test)[i]}, prediction: {preds[i]}")
print("-"*50)
