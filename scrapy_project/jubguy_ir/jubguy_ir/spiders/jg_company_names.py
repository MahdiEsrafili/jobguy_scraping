import scrapy
import json

class JgCompanyNamesSpider(scrapy.Spider):
    name = 'jg_company_names'
    allowed_domains = ['jobguy.ir']
    urls = 'https://api.jobguy.ir/public/company/list/?size=50&index={}'
    start_urls = [urls.format(0)]
    index = 0


    def parse(self, response):
        self.log('=======fetching{}====='.format(self.index))
        data = json.loads(response.text)
        total_company = data['total']
        if data['success']:
            self.index += len(data['data'])
            for company in data['data']:
                item ={
                    'name': company['name']
                }
                yield item
            yield scrapy.Request(url = self.urls.format(self.index), callback=self.parse)

            
        



