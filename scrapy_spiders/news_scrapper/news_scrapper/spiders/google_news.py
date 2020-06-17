# -*- coding: utf-8 -*-
import json
import pandas as pd
import requests
import os
import scrapy
from scrapy.shell import inspect_response

def _get_start_urls():
    return [value for i, value in json_news_data.items() if value != "Error"]
try:
    nasdaq100symbols = json.loads(requests.get("http://127.0.0.1:8000/info/nasdaq_100").text)["symbol"]
    nasdaq100names = json.loads(requests.get("http://127.0.0.1:8000/info/nasdaq_100").text)["companyName"]
    json_news_data = json.loads(requests.get("http://127.0.0.1:8000/info/google_news_links").text)

    start_urls = _get_start_urls()
except:
    print("API ERROR")
    start_urls = []



class GoogleNewsSpider(scrapy.Spider):
    name = 'google_news'
    allowed_domains = ['https://news.google.com/']
    start_urls = start_urls

    def _get_coverage_symbol(self, link):
        for key, value in json_news_data.items():
            if value == link:
                return nasdaq100symbols[nasdaq100names.index(key)]

    def _get_coverage_links(self, Links):
        return [link for link in Links if "/stories/" in link]

    def parse(self, response):
        return_dict = {'index': [],'links': [],'symbols': []}
        links = response.css("a::attr(href)").getall()
        coverages = self._get_coverage_links(links)
        symbol = self._get_coverage_symbol(response.request.url)
        for idx, link in enumerate(coverages):
            return_dict['links'] += [link]
            return_dict['symbols'] += [symbol]
            return_dict['index'] += [idx]

        return_df = pd.DataFrame.from_dict(return_dict)
        return_df.reset_index(drop=True, inplace=True)
        if "news_coverings.csv" in os.listdir("DATA"):
            exists = True
            past_data = pd.read_csv("DATA/news_coverings.csv", sep="|")
        else:
            exists = False
        if exists:
            past_data = past_data.append(return_df)
            past_data = past_data.drop_duplicates()
            past_data.to_csv("DATA/news_coverings.csv", sep="|", index=False)
        else:
            return_df.to_csv("DATA/news_coverings.csv", sep="|", index=False)
            
