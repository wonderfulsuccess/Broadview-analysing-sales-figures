#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from bookinfo.items import BookinfoItem


class AmazonBookSpider(scrapy.Spider):

    name = 'amazonbook'

    def start_requests(self):
        # 爬去计算机和网络图书列表的前N页
        for page in range(1, 11):
            _url = 'https://www.amazon.cn/gp/search/ref=sr_pg_' + str(page) + \
                   '?fst=as%3Aoff&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658414051&page=' + str(page) \
                   + '&sort=popularity-rank&ie=UTF8'
            yield scrapy.Request(url=_url, meta={'current_page': page}, callback=self.parse)

    def parse(self, response):
        page_bool_urls = response.xpath('//img[@alt="产品详细信息"]/../@href').extract()
        print(page_bool_urls)
        for u in page_bool_urls:
            meta_data = {
                'current_page': response.meta['current_page'],
                'index': page_bool_urls.index(u),
            }
            yield scrapy.Request(url=u, meta=meta_data, callback=self.parse_book_detail)

    @staticmethod
    def parse_book_detail(response):
        book_title = response.xpath("//div[@id='dp-container']/div[@id='centerCol']/div[@id='booksTitle']"
                                    "/div[@class='a-section a-spacing-none']/h1[@id='title']"
                                    "/span[1]/text()").extract()
        print(book_title)

        _rankcount = len(response.xpath("//li[@id='SalesRank']/ul/li"))
        _classifies = []
        for i in range(1, _rankcount+1):
            #类型list
            _c = response.xpath("//li[@id='SalesRank']/ul/li[$index]/span[2]/a/text()", index=i).extract()
            _cstr = []
            for _cs in _c:
                _cstr.append(str(_cs))
                _cstr.append('>')
            dic = dict()
            dic[response.xpath("//li[@id='SalesRank']/ul/li[$index]/span[1]/text()", index=i).extract_first()] \
                = ''.join(_cstr[:-1])
            _classifies.append(dic)

        item = BookinfoItem()
        item['coverImage'] = response.xpath("//img[@id='ebooksImgBlkFront']/@src").extract()
        item['classify'] = str(_classifies)
        item['index'] = response.meta['index']
        item['pageNo'] = response.meta['current_page']
        # item['content'] = str(response.body_as_unicode())
        item['content'] = book_title

        yield item
