# -*- coding: utf-8 -*-
import json

import requests

import scrapy
from scrapy.shell import inspect_response

def _get_start_urls():
    return [value for i, value in json_news_data.items() if value != "Error"]

nasdaq100symbols = json.loads(requests.get("http://127.0.0.1:8000/info/nasdaq_100").text)["symbol"]
nasdaq100names = json.loads(requests.get("http://127.0.0.1:8000/info/nasdaq_100").text)["companyName"]
json_news_data = json.loads(requests.get("http://127.0.0.1:8000/info/google_news_links").text)

start_urls = _get_start_urls()



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
        links = response.css("a::attr(href)").getall()
        coverages = self._get_coverage_links(links)
        symbol = self._get_coverage_symbol(response.request.url)
        for link in coverages:
            yield {
                'link': link,
                'symbol': symbol
            }
