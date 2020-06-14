import requests
import json
import pandas as pd
import os


def json_to_dict(data, indicator):
    return_dict = {"Date":[], f"{indicator}_value":[]}
    for key, value in data.items():
        return_dict["Date"].append(key)
        return_dict[f"{indicator}_value"].append(value[indicator])
    return return_dict

indicators = ["SMA", "EMA", "WMA","DEMA","TEMA","TRIMA","KAMA","MAMA","VWAP", "T3","MACD", "MACDEXT","STOCH", "STOCHF","RSI", "STOCHRSI","WILLR","ADX", "ADXR","APO","PPO","MOM","BOP","CCI", "CMO","ROC","ROCR","AROON", "AROONOSC","MFI","TRIX","ULTOSC","DX","MINUS_DI","PLUS_DI","MINUS_DM","PLUS_DM","BBANDS", "MIDPOINT","MIDPRICE","SAR","TRANGE","ATR","NATR","AD","ADOSC","OBV","HT_TRENDLINE","HT_SINE","HT_TRENDMODE","HT_DCPERIOD","HT_DCPHASE","HT_PHASOR"]

symbols = json.loads(open("../DATA/nasdaq100.json", "r+").read())["symbol"]

for symbol in symbols:
    try:
        os.mkdir(f"../DATA/data_per_symbol/{symbol}/CSV/indicators")
    except:
        pass
    for indicator in indicators:
        try:
            response = requests.get(f"https://www.alphavantage.co/query?function={indicator}&symbol={symbol}&interval=weekly&time_period=100&series_type=open&apikey=7Z41ZLKXN0YMG2UG")
            text = json.loads(response.text)
            column = list(text)
            print(column)
            data = text[column[1]]
            dict = json_to_dict(data, indicator)
            df = pd.DataFrame.from_dict(dict)
            df.to_csv(f"../DATA/data_per_symbol/{symbol}/CSV/indicators/{indicator}.csv", sep="@")
            print(f"Done {indicator}, {symbol}")
        except:
            print(f"Error {indicator}, {symbol}")
