import nasdaqAPI
import json
import pandas as pd
# symbols = ["ADI","ADP","ADSK","AMAT","AMGN","AMZN","ANSS","ASML","AVGO","BIDU","BIIB","BKNG","BMRN","CDNS","CDW","CERN","CHKP","CHTR","CMCSA","COST","CPRT","CSCO","CSGP","CSX","CTAS","CTSH","CTXS","DLTR","DXCM","EA","EBAY","EXC","EXPE","FAST","FB","FISV","FOXA","FOX","GILD","GOOG","GOOGL","IDXX","ILMN","INCY","INTC"]

df = pd.read_csv("../DATA/nasdaq-listed-symbols.csv")
symbols = df["Symbol"]

for i in symbols:
    open("nasdaq_data_logs.txt", "w+").write(f"Working on {i}")
    settings = {'SYM':i, 'NWS':24000}
    streamer = nasdaqAPI.NasdaqDataStreamer(settings, verbose=False) 
    data = streamer.run()
    open(f"../DATA/news_articles/{i}_links.json", "w+").write(json.dumps(data['NWS']))
