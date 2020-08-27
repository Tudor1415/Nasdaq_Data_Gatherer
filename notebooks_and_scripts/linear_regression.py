import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# Training on the Apple data
data = pd.read_csv("../DATA/training/stocks/AAPL.csv", sep ="|")

# data["Time"] = [i for i in range(len(data))]
# data["constant"] = [1 for i in range(len(data))]

data.drop("Unnamed: 0", axis=1,inplace=True)
data.drop("TargetProbability", axis=1,inplace=True)
data.drop("prctChangeOPEN", axis=1,inplace=True)

print(data.head())
# data["OPEN"] = data["OPEN"].shift(-30)

IN, IN_test, OUT, OUT_test = train_test_split(data, Target, test_size=0.2, random_state=42)
OUT = np.array(OUT).reshape(OUT.shape[0],1) * 100
OUT_test = np.array(OUT_test).reshape(OUT_test.shape[0],1) * 100

print(f"The shape of our input training data: {IN.shape}")
print(f"The shape of our output training data: {OUT.shape}")
print(f"The shape of our input testing data: {IN_test.shape}")
print(f"The shape of our output testing data: {OUT_test.shape}")

# Since we have enough samples we sill first use the numpy linalg.solve function to do the linear regression
# LINEAR REGRESSION ALGORITHM
print("Started fitting")
# Turing A and b into square matrix
A = np.array(IN).T.dot(IN)
b = np.array(IN).T.dot(OUT)
# Solving the system 
x = np.linalg.lstsq(A,b)[0]
print("Done!")
# print(f"The values for x are: {x}")
print("-"*50)
preds = np.array(IN_test).dot(x)
mse = np.square(preds - OUT_test).mean(axis=0)
print(f"Testing, the mse is: {mse[0]}!")
for i in np.random.randint(0,350, size=(20,1)):
    print(f"True value: {np.array(OUT_test)[i][0][0]}, prediction: {preds[i][0][0]}")
print("-"*50)



