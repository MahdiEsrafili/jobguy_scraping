import scrapy


class JgCommentTitleSpider(scrapy.Spider):
    name = 'jg_comment_title'
    allowed_domains = ['jobguy.ir']
    start_urls = ['https://jobguy.ir/company/rahkar-hoshmand-iranian']

    def parse(self, response):
        comments = response.css('div.el-card__body >div.layout-v')
        for comment in comments:
            item = {
                'company' : response.css('h1::text').extract_first(),
                'title': comment.css('div.header >div.layout-h >h3.title >a::text').extract(),
                'description': comment.css('div.wrap-contetn >div.desc >div.description-te::text').extract(),

            }
            yield item
