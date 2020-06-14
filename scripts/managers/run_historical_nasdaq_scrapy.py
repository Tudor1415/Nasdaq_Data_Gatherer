import requests
import os
import json

symbols = json.loads(requests.get("http://127.0.0.1:8000/info/nasdaq_100").text)["symbol"]

for symbol in symbols:
    os.chdir("../../scrapy_spiders/news_scrapper/")
    os.system(f"scrapy crawl nasdaq_news -a symbol={symbol}")
