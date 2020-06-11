import nasdaqAPI
from helpers import get_nasdaq100
import json

symbols = get_nasdaq100()[1]['symbol']

for i in symbols:
    print(i)
    settings = {'SYM':i, 'NWS':2400}
    streamer = nasdaqAPI.NasdaqDataStreamer(settings) 
    data = streamer.run()
    open(f"DATA/news_articles/{i}.json", "w+").write(json.dumps(data['NWS']))
    print(f"Done {i}!") 