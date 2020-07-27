import scrapy
import json
import pandas as pd
class CompanyCommentsSpider(scrapy.Spider):
    name = 'company_comments'
    allowed_domains = ['jobguy.ir']
    urls = 'https://api.jobguy.ir/public/company/list/?size=50&index={}'
    start_urls = [urls.format(0)]
    index = 0
    base_url = 'https://jobguy.ir/company/'
    comment_index = 1
    # dataframe = pd.DataFrame(columns = ['comapny', 'title', 'description'])
    
    def parse(self, response):
        self.log('=======fetching{}====='.format(self.index))
        data = json.loads(response.text)
        total_company = data['total']
        if data['success']:
            self.index += len(data['data'])
            for company in data['data']: 
                if company['total_review'] + company['total_interview'] >0:
                    yield scrapy.Request(url = self.base_url + company['company_slug'], callback= self.comment_parser )

            yield scrapy.Request(url = self.urls.format(self.index), callback=self.parse)
            # self.dataframe.to_csv('jobguy_data.csv', mode='a')
        

    def comment_parser(self, response):
        comments = response.css('div.el-card__body >div.layout-v')
        for comment in comments:
            url = comment.css('div.header >div.layout-h >h3.title >a::attr(href)').extract_first()
            yield scrapy.Request(url =response.urljoin(url), callback= self.detail_page )
            # item = {
            #     'index' : [self.comment_index],
            #     'company' : response.css('h1::text').extract(),
            #     'title': comment.css('div.header >div.layout-h >h3.title >a::text').extract(),
            #     'description': comment.css('div.wrap-contetn >div.desc >div.description-te::text').extract(),

            # }
            # # yield item
            # dataframe= pd.DataFrame(item)
            # dataframe.to_csv('jobguy_data.csv', mode= 'a', encoding='utf-8', header=False)
            # self.comment_index += 1

    def detail_page(self, response):
        company = response.css('div.details >h1::text').extract()
        title = response.css('h3.title >a::text').extract()
        description= response.css('div.description-te>p::text').extract()
        url = [response.url]
        self.log('=====================company: {}, title: {}, desc: {}'.format(len(company),len(title),len(description)))
        if len(title)==0:
            title = ['NULL']
        if len(description)>1:
            description = [' '.join(description)]
        elif len(description) ==0:
            description = ['NULL']
        
        if len(company)==0:
            company = response.css('div.details >h2::text').extract()
        # if company=
        # self.log(co)
        item = {
            'company' : company,
            'title' :title,
            'description' : list(description),
            'url' : url,
        }
        dataframe= pd.DataFrame(item)
        dataframe.to_csv('jobguy_data_2.csv', mode= 'a', encoding='utf-8', header=False)