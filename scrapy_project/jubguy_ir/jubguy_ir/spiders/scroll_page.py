import scrapy
import json

class ScrollPageSpider(scrapy.Spider):
    name = 'scroll_page'
    allowed_domains = ['toscrape.com']
    page_url = 'http://quotes.toscrape.com/api/quotes?page={}'
    start_urls = [page_url.format(1)]

    def parse(self, response):
        data = json.loads(response.text)
        for quote in data['quotes'] : 
            yield {
                'author_name' : quote['author']['name'],
                'text' : quote['text']
                }
        if data['has_next']:
            yield scrapy.Request(url = self.page_url.format(data['page']+1), callback=self.parse)
