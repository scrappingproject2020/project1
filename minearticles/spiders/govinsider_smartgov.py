# -*- coding: utf-8 -*-
import scrapy


class GovinsiderSmartgovSpider(scrapy.Spider):
    name = 'govinsider_smartgov'
    allowed_domains = ['govinsider.asia']
    start_urls = ['https://www.govinsider.asia/smart-gov']

    def parse(self, response):
        articles = response.xpath("//h2[contains(@class,'entry-title')]")
        for article in articles:
            title = article.xpath(".//a/text()").get()
            link = article.xpath(".//a/@href").get()
            blurp = article.xpath(".//parent::div/div[contains(@class,'entry-summary')]/p/text()").get()
            article_url = f"https://govinsider.asia{link}"
            yield response.follow(url=link, callback=self.parse_article, meta={'article_title': title, 'url': article_url, 'blurp': blurp})

            
    def parse_article(self,response):
            title = response.request.meta['article_title']
            url = response.request.meta['url']
            blurp = response.request.meta['blurp']
            paragraphs = response.xpath("//div[@class='entry-content post-content']/p")
            text =''
            
            for para in paragraphs:
                para_text = para.xpath(".//text()").get()
                        
                if para_text is not None:
                    text = text + para_text
            
            yield {
                'title': title,
                'blurp' : blurp,
                'text': text,
                'url': url
            }