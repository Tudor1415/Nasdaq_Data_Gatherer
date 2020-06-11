import json

import yfinance as yf

symbols = ['CERN', 'FOXA', 'MU', 'AAPL', 'ADBE', 'ADI', 'ADP', 'ADSK', 'ALGN', 'ALXN', 'AMAT', 'AMD', 'AMGN', 'AMZN', 'ANSS', 'ASML', 'ATVI', 'AVGO', 'BIDU', 'BIIB', 'BKNG', 'BMRN', 'CDNS', 'CDW', 'CHKP', 'CHTR', 'CMCSA', 'COST', 'CPRT', 'CSCO', 'CSGP', 'CSX', 'CTAS', 'CTSH', 'CTXS', 'DLTR', 'DXCM', 'EA', 'EBAY', 'EXC', 'EXPE', 'FAST', 'FB', 'FISV', 'FOX', 'GILD', 'GOOG', 'GOOGL', 'IDXX', 'ILMN', 'INCY', 'INTC', 'INTU', 'ISRG', 'JD', 'KHC', 'KLAC', 'LBTYA', 'LBTYK', 'LRCX', 'LULU', 'MAR', 'MCHP', 'MDLZ', 'MELI', 'MNST', 'MSFT', 'MXIM', 'NFLX', 'NTAP', 'NTES', 'NVDA', 'NXPI', 'ORLY', 'PAYX', 'PCAR', 'PEP', 'PYPL', 'QCOM', 'REGN', 'ROST', 'SBUX', 'SGEN', 'SIRI', 'SNPS', 'SPLK', 'SWKS', 'TCOM', 'TMUS', 'TSLA', 'TTWO', 'TXN', 'UAL', 'ULTA', 'VRSK', 'VRSN', 'VRTX', 'WBA', 'WDAY', 'WDC', 'XEL', 'XLNX', 'ZM']
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