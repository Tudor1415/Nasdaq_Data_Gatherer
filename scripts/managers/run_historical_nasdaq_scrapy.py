import requests
import os
import json

symbols = json.loads(requests.get("http://127.0.0.1:8000/info/nasdaq_100").text)["Symbol"]

for symbol in symbols:
    print(f"Working on {symbol}")
    open("logs.txt", "w+").write(f"Working on {symbol}")
    os.chdir("../../scrapy_spiders/news_scrapper/")
    os.system(f"scrapy crawl nasdaq_news -a symbol={symbol}")
    print(f"Finished {symbol}")
