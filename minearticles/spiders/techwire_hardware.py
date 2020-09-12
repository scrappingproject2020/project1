# -*- coding: utf-8 -*-
import scrapy


class TechwireHardwareSpider(scrapy.Spider):
    name = 'techwire_hardware'
    allowed_domains = ['www.techwireasia.com/tag/hardware']
    start_urls = ['https://www.techwireasia.com/tag/hardware/']

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

        text =''
        for para in paragraphs:
            current = para.xpath(".//text()").get()
            if current is not None: 
                text = text + current

        blurp = text.split('.')[:4]

        yield {
             'category': 'Hardware',
             'blurp' : blurp,
             'imgrul': imgurl,
             'text': text,
             'title': title,
             'url': url,
             'date': article_date
         }