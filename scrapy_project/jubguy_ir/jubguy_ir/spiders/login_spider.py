import scrapy


class LoginSpiderSpider(scrapy.Spider):
    name = 'login_spider'
    allowed_domains = ['toscrape.com']
    login_url = 'http://quotes.toscrape.com/login'
    start_urls = [login_url]


    def parse(self, response):
        token = response.css('input[name=csrf_token]::attr(value)').extract_first()
        login_data = {
            'csrf_token':token,
            'username' : 'abc',
            'password' : 'abc',
        }
        yield scrapy.FormRequest(url = self.login_url,formdata = login_data, callback=self.login)

    def login(self, response):
        for quote in response.css('div.quote') :
            item= {
                'author_name' : quote.css('small.author::text').extract(),
                'text' : quote.css('span.text::text').extract(),
                'tag' : quote.css('a.tag::text').extract(),
            }
            yield item
