




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



class ArticlesSpider(scrapy.Spider):
    
    name = "infoworld"
    download_delay = 5.0
    handle_httpstatus_list = [200]
    def start_requests(self):
        catdict = {'machine-learning': {'4049' :"4995,4825"}, 
            'software-development': {'3646':"3646,4403,3443,3808,3469,3761,4434,3470,3881,4047,3471"},
            'cloud-computing':{'3255':"4309,3374,3375,3378,3712,4774"}, 
            'analytics':{'3551':"3256,3474,3781,3408,4048"}}
        API_URL = 'https://www.infoworld.com/napi/tile?'
        for topic in catdict: 
            for catid in catdict[topic]:     
        #     Get parameters
                params = {
                    'def': 'loadMoreList',
                    'pageType' : 'index',
                    'catId' : catid,
                    'includeMediaResources': False,
                    'createdTypeIds': 1,
                    'categories': catdict[topic][catid],
                    'days':-730,
                    'pageSize':1000,
                    'Offset' : 0,
                    'ignoreExcludedIds': True,
                    'brandContentOnly': False,
                    'includeBlogTypeIds': "1,3",
                    'includeVideo' : False,
                    'sortOrder': "date",
                    'locale_id': 0,
                    'startIndex': 0
                    }
                # response = requests.get(API_URL, params=params)
                response = scrapy.Request(add_or_replace_parameters(API_URL, params))
                # response = TextResponse(body = response.content, url = API_URL)
                # output = self.parse_main_pages(response)

                yield(response)

    def parse(self, response):
        title={}
        content=response.xpath('//div[@class="river-well article"]')
        for article_link in content.xpath('.//h3//a'):
                article_url=   article_link.xpath('.//@href').extract_first()
                article_title =article_link.xpath('./text()').extract_first()
                
                if article_url.startswith("/article/"):
                    # title['article_title']=article_title
                    # title['article_link'] = "https://www.infoworld.com" + article_url    
                    title[article_title] =  "https://www.infoworld.com" +  article_url
                
        yield(title)
