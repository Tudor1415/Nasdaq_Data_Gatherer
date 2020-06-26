import json
import pandas as pd
import yfinance as yf

df = pd.read_csv("../DATA/nasdaq-listed-symbols.csv")
symbols =df["Symbol"]
errors = 0
for i in symbols:
    try:
        stock = yf.Ticker(i)
        stock.sustainability.to_json(f"../DATA/data_per_symbol/{i}/sustainability.json")
        print(i)
    except:
        print(f"Error: {errors}")
        errors += 1 

    try:
        stock = yf.Ticker(i)
        stock.recommendations.to_json(f"../DATA/data_per_symbol/{i}/recommendations.json")
        print(i)
    except:
        print(f"Error: {errors}")
        errors += 1 