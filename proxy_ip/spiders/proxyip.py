# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib import parse
import json
from proxy_ip.items import ProxyIpItem
class ProxyipSpider(scrapy.Spider):
    name = 'proxyip'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0']
    origin_num = 0
    #next_url = ''
    def parse(self, response):
        yield Request(url=parse.urljoin(response.url,self.start_urls[0]),callback=self.parse_detail,dont_filter=True)

    def parse_detail(self,response):
        movie_rank = ProxyIpItem()
        result = response.text
        items = json.loads(result).get("subjects","")

        # if items:
        #     self.origin_num = self.origin_num +1
        #     url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start={0}'
        #     global next_url
        #     next_url = url.format(self.origin_num*20)
        for item in items:
            rate = item.get("rate","")
            url = item.get("url","")

            movie_rank["rate"] = rate
            movie_rank["url"] = url
            yield movie_rank
       # yield  Request(url=parse.urljoin(response.url,next_url),callback=self.parse_detail,dont_filter=True)