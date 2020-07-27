import scrapy


class SecondSpider(scrapy.Spider):
    name = 'second'
    allowed_domains = ['toscrape.com']
    start_urls = ['https://quotes.toscrape.com']

    def parse(self, response):
        for quote in response.css('div.quote') :
            item= {
                'author_name' : quote.css('small.author::text').extract(),
                'text' : quote.css('span.text::text').extract(),
                'tag' : quote.css('a.tag::text').extract(),
            }
            yield item
        
        # following next page:
        next_url = response.css('li.next >a ::attr(href)').extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(url = next_url, callback= self.parse)
