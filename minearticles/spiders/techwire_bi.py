# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime

class TechwireBiSpider(scrapy.Spider):
    name = 'techwire_bi'
    allowed_domains = ['www.techwireasia.com/tag/business-intelligence']
    start_urls = ['https://techwireasia.com/tag/business-intelligence/']

    def parse(self, response):
        # articles = response.xpath("//div[@class='large-6 medium-6 columns panel']")
        articles = response.xpath("//header[@class='article-header']")

        for article in articles:
            title = article.xpath(".//h3/a/text()").get()
            link = article.xpath(".//h3/a/@href").get()
            yield response.follow(url=link, callback=self.parse_article, dont_filter=True, meta={'article_title': title, 'url': link})


    def parse_article(self,response):
        title = response.request.meta['article_title']
        url = response.request.meta['url']
        paragraphs = response.xpath("//div[contains(@class, 'large-7 medium-7 columns single-content')]/p")
        imgurl = response.xpath("//div[@class='main-post-thumbnail']//img/@src").get()

        article_date = response.xpath("//div[@class='details']//text()").getall()
        article_date = article_date[2]
        article_date = article_date.replace("|", "").lstrip()
        article_date = article_date.replace(",", "")
        article_date = datetime.strptime(article_date, '%d %B %Y') 

        text =''
        for para in paragraphs:
            current = para.xpath(".//text()").get()
            if current is not None: 
                text = text + current

        blurp = "".join(text.split('.')[:4])

        yield {
             #'category': 'Business Intelligence',
             'title': title,
             'imgrul': imgurl,
             'date': article_date,
             'blurp' : blurp,
             'url': url,
             'text': text
         }
