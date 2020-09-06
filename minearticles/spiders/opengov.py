# -*- coding: utf-8 -*-
import scrapy
import time

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
            blurp = "Article has not blurp"
            time.sleep(2)
            yield response.follow(url=link, callback=self.parse_article, dont_filter=True, meta={'article_title': title, 'url': link, 'blurp': blurp})


    def parse_article(self,response):
        title = response.request.meta['article_title']
        url = response.request.meta['url']
        blurp = response.request.meta['blurp']
        paragraphs = response.xpath("//div[contains(@class, 'main_post_content')]/div/p")
        imgurl = response.xpath("//div[contains(@class, 'main_post_content')]/preceding-sibling::div[contains(@class,'image')]/div//img/@src").get()

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
