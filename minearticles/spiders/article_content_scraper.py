import json
import scrapy



class ArticlescraperSpider(scrapy.Spider):
    name = 'ArticleScraper'
    start_urls =['https://www.infoworld.com']
    def start_requests(self):
        with open('articles.json') as json_file:
            data = json.load(json_file)
            for i in range(0,4):
                for article in data[i]:
                    print(data[i][article])
                    request=scrapy.Request(data[i][article],cookies={'store_language':'en'}, callback=self.parse_article_pages,meta={'url':data[i][article]})
                    if request:
                        yield request
    


    def parse_article_pages(self, request):
        item ={}
        a_body=""
        # Extracts the article_body in <p> <li> elements
        # for p in request.xpath('//div[starts-with(@class,"cat ")]//p/text()').extract():
        title = request.xpath('//h1[@itemprop="headline"]//text()').extract()
        # a_body = request.xpath('//div[@class="cat "]/descendant::text()').extract()
        blurp = request.xpath('//h3[@itemprop="description"]//text()').extract()
        #a_body = request.xpath('//div[@itemprop="articleBody"]//p/text()').get()
        a_body = request.xpath('//div[@itemprop="articleBody"]/descendant::text()').extract()
        # print(p)
        # a_body=a_body+p
        if a_body:
            item['article_title'] =title
            item['article_body']= a_body
            item['blurp']=blurp
            item['url']= request.meta['url']
        yield (item)
