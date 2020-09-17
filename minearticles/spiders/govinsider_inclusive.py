# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime

class GovinsiderSmartgovSpider(scrapy.Spider):
    name = 'govinsider_inclusive'
    allowed_domains = ['govinsider.asia']
    start_urls = ['https://www.govinsider.asia/inclusive-gov']
    next_page = 2

    def parse(self, response):
        articles = response.xpath("//h2[contains(@class,'entry-title')]")
        for article in articles:
            title = article.xpath(".//a/text()").get()
            link = article.xpath(".//a/@href").get()
            blurp = article.xpath(".//parent::div/div[contains(@class,'entry-summary')]/p/text()").get()
            article_url = f"https://govinsider.asia{link}"
            yield response.follow(url=link, callback=self.parse_article, meta={'article_title': title, 'url': article_url, 'blurp': blurp})

        # get next page, currently stop at second page
        
        if self.next_page <= 2:
            full_url = f"https://govinsider.asia/smart-gov/page/{self.next_page}/"
            self.next_page += 1
            yield scrapy.Request(url=full_url, callback = self.parse)

            
    def parse_article(self,response):
            title = response.request.meta['article_title']
            url = response.request.meta['url']
            blurp = response.request.meta['blurp']
            img = response.xpath("//div[@class='col-sm-9 post-content-col']/img/@src").get()
            imgurl = f"https://govinsider.asia{img}"

            paragraphs = response.xpath("//div[@class='entry-content post-content']/p")
            text =''
            
            for para in paragraphs:
                para_text = para.xpath(".//text()").get()
                        
                if para_text is not None:
                    text = text + para_text
            
            article_date = response.xpath("//time[@class='updated']/text()").get()
            article_date = datetime.strptime(article_date, '%d %b %Y')

            yield {
                'title': title,
                'imgrul': imgurl,
                'date': article_date, 
                'blurp' : blurp,
                'url': url,
                'text': text
            }