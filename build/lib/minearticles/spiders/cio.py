# -*- coding: utf-8 -*-
import scrapy
import logging

class CioSpider(scrapy.Spider):
    name = 'cio'
    allowed_domains = ['www.cio.com']
    start_urls = ['https://www.cio.com/asean/category/analytics']
    

    def parse(self, response):
        articles = response.xpath("//div[@class='main-col']/div")
        for article in articles[3:]:
            title = article.xpath(".//div/h3/a/text()").get()
            link = article.xpath(".//div/h3/a/@href").get()
            blurp = article.xpath(".//div/h4/text()").get()
            article_url = f"https://www.cio.com{link}"            
            yield response.follow(url=link, callback=self.parse_article, meta={'article_title': title, 'url': article_url, 'blurp': blurp})

        # get next page at the moment, doing 3 hops by specify start=80
        next_page = response.xpath("//a[@id='load-more-index']/@href").get()
        
        if next_page and next_page != '?start=80':
            full_url = f"https://www.cio.com/asean/category/analytics/{next_page}"
            yield scrapy.Request(url=full_url, callback = self.parse)
        
    def parse_article(self,response):
        title = response.request.meta['article_title']
        url = response.request.meta['url']
        blurp = response.request.meta['blurp']
        paragraphs = response.xpath("//div[@itemprop='articleBody']/p")
        text =''
        for para in paragraphs:
            text = text + para.xpath(".//text()").get()

        yield {
             'title': title,
             'blurp' : blurp,
             'text': text,
             'url': url
         }
    