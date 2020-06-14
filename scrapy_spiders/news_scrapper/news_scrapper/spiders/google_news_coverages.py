# -*- coding: utf-8 -*-
import scrapy
import json
import requests

coverages_links = ['https://news.google.com/' + i["link"].split("./")[1] for i in json.loads(requests.get("http://127.0.0.1:8000/info/training_news_coverings").text)]

class GoogleNewsCoveragesSpider(scrapy.Spider):
    name = 'google_news_coverages'
    allowed_domains =  ['https://news.google.com/']
    start_urls = coverages_links

    def parse(self, response):
        links = response.css("h4 > a::attr(href)").getall()
        titles = response.css("h4 > a::text").getall()
        for i, link in enumerate(links):
            yield {
                'link': link,
                'title': titles[i],
                'coverage_link': response.request.url
            }