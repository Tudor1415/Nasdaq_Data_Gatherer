# -*- coding: utf-8 -*-
import scrapy
import json
import requests
import os

symbols = json.loads(requests.get("http://127.0.0.1:8000/info/nasdaq_100").text)["symbol"]

class NasdaqNewsSpider(scrapy.Spider):
    name = 'nasdaq_news'
    allowed_domains = ['nasdaq.com']
    def __init__(self, symbol='', **kwargs):
        self.symbol = symbol
        self.start_urls = json.loads(requests.get(f"http://127.0.0.1:8000/info/nasdaq_historical_news_links/{symbol}").text)["Link"]
        super().__init__(**kwargs) 

    def parse(self, response):
        text = "".join(response.css("div.body:nth-child(3) > div:nth-child(2)").css("p::text").getall())
        title = response.css("h1 > span::text").get()
        published_date = response.css("time::text").get()
        return_dict = {
            'Content': text,
            'Title': title,
            'Published_Date': published_date,
            'Link': response.request.url
        }
        open(f"{self.symbol}.json", "w+").write(json.dumps(return_dict))