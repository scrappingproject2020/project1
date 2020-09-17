# -*- coding: utf-8 -*-
import scrapy
import re
from datetime import datetime

class OpengovHealthcareSpider(scrapy.Spider):
    name = 'opengov_healthcare'
    allowed_domains = ['www.opengovasia.com']
    start_urls = ['https://www.opengovasia.com/healthcare']

       
    def parse(self, response):
        
        articles = response.xpath("//div[@class='elementor-post__text']")
        otherarticles = response.xpath("//h1[@class='elementor-heading-title elementor-size-default']")
        
        for article in articles:
            title = article.xpath(".//h3/a/text()").get().lstrip()
            link = article.xpath(".//h3/a/@href").get()
            link = link.replace("http://","https://")
            yield response.follow(url=link, callback=self.parse_article, meta={'article_title': title, 'url': link}, dont_filter=True)

        for article in otherarticles:
            title = article.xpath(".//a/text()").get().lstrip()
            link = article.xpath(".//a/@href").get()
            link = link.replace("http://","https://")
            yield response.follow(url=link, callback=self.parse_article, meta={'article_title': title, 'url': link}, dont_filter=True)


    def parse_article(self,response):
        title = response.request.meta['article_title']
        url = response.request.meta['url']
        paragraphs = response.xpath("//div[contains(@class, 'theme-post-content')]/div/p")
        imgurl = response.xpath("//div[contains(@class, 'theme-post-content')]/preceding-sibling::div[contains(@class,'image')]/div//img/@src").get()
        article_date = response.xpath("//span[contains(@class,'item--type-date')]/text()").get()
               
        regex = re.compile(r'[\n\t,]')
        article_date = regex.sub("", article_date)
        article_date = article_date.lstrip()
        article_date = datetime.strptime(article_date, '%B %d %Y') 
       

        text =''
        for para in paragraphs:
            current = para.xpath(".//text()").get()
            if current is not None:
                text = text + current
        
        blurp = "".join(text.split(".")[:4])

        yield {
             #'category': 'Health Care',
             'title': title,
             'imgrul': imgurl,
             'date': article_date,
             'blurp' : blurp,
             'url': url,
             'text': text
         }