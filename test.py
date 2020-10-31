import yfinance as yf
import pandas 


def on_get(symbol):
    stock = yf.Ticker(symbol.upper())
    df = stock.history(period="max")
    df.index = df.index.strftime('%Y-%m-%d')
    data = df.to_dict()
    return data

print(on_get("AAPL"))