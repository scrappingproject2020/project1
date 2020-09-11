# -*- coding: utf-8 -*-
import scrapy
import time
import re

class OpengovSpider(scrapy.Spider):
    name = 'opengov'
    allowed_domains = ['www.opengovasia.com']
    start_urls = ['https://www.opengovasia.com']

    def parse(self, response):
        
        articles = response.xpath("//div[@class='elementor-post__text']")
        
        for article in articles:
            title = article.xpath(".//h3/a/text()").get().lstrip()
            link = article.xpath(".//h3/a/@href").get()
            link = link.replace("http://","https://")
            time.sleep(2)
            yield response.follow(url=link, callback=self.parse_article, dont_filter=True, meta={'article_title': title, 'url': link})


    def parse_article(self,response):
        title = response.request.meta['article_title']
        url = response.request.meta['url']
        paragraphs = response.xpath("//div[contains(@class, 'main_post_content')]/div/p")
        imgurl = response.xpath("//div[contains(@class, 'main_post_content')]/preceding-sibling::div[contains(@class,'image')]/div//img/@src").get()
        
        article_date = response.xpath("//span[contains(@class,'item--type-date')]/text()").get()
               
        regex = re.compile(r'[\n\t]')
        article_date = regex.sub("", article_date)
        article_date = article_date.lstrip()
       

        text =''
        for para in paragraphs:
            current = para.xpath(".//text()").get()
            if current is not None:
                text = text + current
        
        blurp = text[0:150]

        yield {
             'category': 'None',
             'blurp' : blurp,
             'imgrul': imgurl,
             'text': text,
             'title': title,
             'url': url,
             'date': article_date
         }
