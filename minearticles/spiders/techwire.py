# -*- coding: utf-8 -*-
import scrapy


class TechwireSpider(scrapy.Spider):
    name = 'techwire'
    allowed_domains = ['www.techwireasia.com/']
    start_urls = ['https://www.techwireasia.com/']

    def parse(self, response):
        # articles = response.xpath("//div[@class='large-6 medium-6 columns panel']")
        articles = response.xpath("//header[@class='article-header']")

        for article in articles:
            title = article.xpath(".//h3/a/text()").get()
            link = article.xpath(".//h3/a/@href").get()
            blurp = "TechWire has no blurp"
            yield response.follow(url=link, callback=self.parse_article, dont_filter=True, meta={'article_title': title, 'url': link, 'blurp': blurp})


    def parse_article(self,response):
        title = response.request.meta['article_title']
        url = response.request.meta['url']
        blurp = response.request.meta['No blurp for this article']
        paragraphs = response.xpath("//div[contains(@class, 'large-7 medium-7 columns single-content')]/p")
        imgurl = response.xpath("//div[@class='main-post-thumbnail']//img/@src").get()
        
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

