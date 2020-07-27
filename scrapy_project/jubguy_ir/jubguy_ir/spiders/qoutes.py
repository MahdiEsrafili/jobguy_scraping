import scrapy


class QoutesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['toscrape.py']
    start_urls = ['http://quotes.toscrape.com/random']

    def parse(self, response):
        self.log('url visited:\t'+ response.url)
        yield {
            'auther_name': response.css('small.auther::text').extract_first(),
            'text': response.css('span.text::text').extract_first(),
            'tags': response.css('a.tag::text').extract_first(),
        }
