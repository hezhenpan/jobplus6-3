# -*- coding: utf-8 -*-

import scrapy

class DataSpider(scrapy.Spider):
    name = 'data'
    start_urls = ['https://www.zhipin.com/?ka=header-home']

    def parse(self, response):
        for url in response.xpath('//ul[@class="cur"]/li/div[@class="sub-li"]/a/@href').extract():
            yield response.follow(url, callback=self.crawl_parse)

    def crawl_parse(self, response):
        data = {
            'company_name': response.xpath('//h1[@class="name"]/text()').extract_first(),
            'company_logo': response.xpath('//div[@class="company-logo"]/img/@src').extract_first(),
            'company_locate': response.xpath('//div[@class="business-detail"]/ul/li[6]/text()').extract_first(),
            'phone': '123456789',
            'website': 'www.shiyanlou.com',
            'desc_simple': response.xpath('//div[@class="business-detail"]/ul/li[8]/text()').extract_first(),
            'desc_more': 'more data need to crawl'
        }


        jobs = {}
        for box in response.xpath('//div[@class="info-primary"]'):
            info = {
                'salary': box.xpath('.//span[@class="salary"]/text()').extract_first(),
                'others': box.xpath('.//p[@class="gray"]/text()').extract_first()
            }
            job_name = box.xpath('.//b/text()').extract_first()
            jobs[job_name] = info
        data['jobs'] = jobs

        yield data
