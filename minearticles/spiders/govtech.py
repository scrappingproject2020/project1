




# Spider 1 
# Articles.py which scrape article links
# imports
import scrapy
from scrapy.http import Request
from w3lib.url import add_or_replace_parameters
import json
import requests
from scrapy.http import Request
from scrapy.http import TextResponse
# class ArticlesSpider(scrapy.Spider):
#     name = 'Articles'
#     allowed_domains = ['infoworld.com']
#     start_urls = ['https://www.infoworld.com/]



class GovtechSpider(scrapy.Spider):
    
    name = "govtech"
    download_delay = 5.0
    handle_httpstatus_list = [200]
    def start_requests(self):
        URL = 'https://www.govtech.com/'
        response = requests.get(URL)
        response =TextResponse(body = response.text, url = URL, encoding='utf-8')
        content = response.xpath('//div[@class="sub-feature-article"]')
        for article_link in content.xpath('.//h2//a'):
            article_url=article_link.xpath('.//@href').get()
            article_url = article_url.split('?')[0]
            title=article_link.xpath('.//text()').get()
            print(article_url)
            yield(scrapy.Request(url=article_url, callback=self.parse_article, meta={'article_title': title, 'url': article_url}))

    def parse_article(self, response):
        item ={}
        item['title'] = response.meta['article_title'] 
        item['url'] = response.meta['url'] 
        item['blurp'] = response.xpath('//p[@class="description"]//text()').get()
        item['text']=  ''.join(response.xpath('//div[@id="article_body"]//p//text()').extract())
        item['img_url'] = 'https:' + response.xpath('//div[@id="feature_image"]//amp-img//@src').get()    
        item['date'] = response.xpath('//div//span[@class="date"]//text()') .get().strip()    
        print(item)
        yield(item)

    
