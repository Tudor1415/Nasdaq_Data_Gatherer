# -*- coding: utf-8 -*-
import scrapy
import json
import requests
import os

symbols = json.loads(requests.get("http://127.0.0.1:8000/info/nasdaq_100").text)["symbol"]

class NasdaqNewsSpider(scrapy.Spider):
    name = 'nasdaq_news'
    allowed_domains = ['nasdaq.com']
    start_urls = ['https://www.nasdaq.com/articles/u.s.-states-lean-toward-breaking-up-googles-ad-tech-business-cnbc-2020-06-05-0']

    def parse(self, response):
        for symbol in symbols:
            self.start_urls =  ['https://news.google.com/' + i["link"].split("./")[1] for i in json.loads(requests.get(f"http://127.0.0.1:8000/info/nasdaq_historical_news_links/{symbol}").text)]
            text = "".join(response.css("div.body:nth-child(3) > div:nth-child(2)").css("p::text").getall())
            title = response.css("h1 > span::text").get()
            published_date = response.css("time::text").get()
            return_dict = {
                'Content': text,
                'Title': title,
                'Published_Date': published_date,
                'Link': response.request.url
            }
            open(f"{symbol}.json", "w+").write(json.dumps(return_dict))