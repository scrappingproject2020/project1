import json
import scrapy
import datetime


class ArticlescraperSpider(scrapy.Spider):
    name = 'ArticleScraper'
    start_urls =['https://www.infoworld.com']
    def start_requests(self):
        with open('articles_url_topic.json') as json_file:
            data = json.load(json_file)
            for i in range(0,4):
                topic = list(data[i].keys())[0]
                print(topic)
                for article in data[i][topic]:
                    # print(data[i][article])
                    request=scrapy.Request(data[i][topic][article],cookies={'store_language':'en'}, callback=self.parse_article_pages,meta={'url':data[i][topic][article], 'topic' : topic})
                    if request:
                        yield request
    


    def parse_article_pages(self, request):
        item ={}
        a_body=""
        #extract image
        image = request.xpath('//img[@itemprop="contentUrl"]/@data-original').get()
        title = request.xpath('//h1[@itemprop="headline"]//text()').get()
        #get date
        date = request.xpath('//span[@class="pub-date"]/@content').get()
        date =date.split('T')[0]
        #get the blurp
        blurp = request.xpath('//h3[@itemprop="description"]//text()').get()
        #a_body = request.xpath('//div[@itemprop="articleBody"]//p/text()').get()
        a_body = ''.join(request.xpath('//div[@itemprop="articleBody"]/descendant::text()').extract()).strip()
        # print(p)
        # a_body=a_body+p
        if a_body:
            item['article_title'] =title
            item['image']=image
            item['date'] =date
            item['topic']= request.meta['topic']
            item['blurp']=blurp
            item['url']= request.meta['url']
            item['article_body']= a_body
        yield (item)
