# -*- coding: utf-8 -*-
import scrapy
import logging

class CioSpider(scrapy.Spider):
    name = 'cio_cloud'
    allowed_domains = ['www.cio.com']
    start_urls = ['https://www.cio.com/asean/category/cloud-computing']
    

    def parse(self, response):
        articles = response.xpath("//div[@class='main-col']/div")
        for article in articles[3:]:
            title = article.xpath(".//div/h3/a/text()").get()
            link = article.xpath(".//div/h3/a/@href").get()
            blurp = article.xpath(".//div/h4/text()").get()
            article_url = f"https://www.cio.com{link}"            
            yield response.follow(url=link, callback=self.parse_article, meta={'article_title': title, 'url': article_url, 'blurp': blurp})

        # get next page at the moment, doing 2 hops by specify start=40
        next_page = response.xpath("//a[@id='load-more-index']/@href").get()
        
        if next_page and next_page != '?start=40':
            full_url = f"https://www.cio.com/asean/category/cloud-computing/{next_page}"
            yield scrapy.Request(url=full_url, callback = self.parse)
        
    def parse_article(self,response):
        title = response.request.meta['article_title']
        url = response.request.meta['url']
        blurp = response.request.meta['blurp']
        paragraphs = response.xpath("//div[@itemprop='articleBody']/p")
        #img = response.xpath("//div[@class='col-sm-9 post-content-col']/img/@src").get()
        imgurl = response.xpath(".//img/@data-original").get()

        text =''
        for para in paragraphs:
            text = text + para.xpath(".//text()").get()

        yield {
             'title': title,
             'blurp' : blurp,
             'text': text,
             'url': url,
             'imgrul': imgurl
         }
