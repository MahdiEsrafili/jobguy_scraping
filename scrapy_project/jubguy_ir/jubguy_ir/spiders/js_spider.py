import scrapy
from scrapy_splash import SplashRequest

class JsSpiderSpider(scrapy.Spider):
    name = 'js_spider'
    def start_requests(self):
        yield  SplashRequest(url = 'http://quotes.toscrape.com/js', callback= self.parse)

    def parse(self, response):
        for quote in response.css('div.quote') :
            yield {
                'text' : quote.css('span.text::text').extract_first(),
                'author_name' : quote.css('small.author::text').extract_first(),
            }
