import scrapy
import json
import pandas as pd
from scrapy_splash import SplashRequest

class ProsConsSpider(scrapy.Spider):
    name = 'pros_cons'
    allowed_domains = ['jobguy.ir']
    urls = 'https://api.jobguy.ir/public/company/list/?size=50&index={}'
    start_urls = [urls.format(0)]
    index = 0
    base_url = 'https://jobguy.ir/company/'
    comment_index = 1
    company_slug = [' ']
    
    dataframe= pd.DataFrame(columns =['company_slug','company','title', 'pros',
    'cons','mean_salary','comment','url','tell_friend', 'like', 'dislike', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'type'])
    dataframe.to_csv('jobguy_pros_cons.csv', mode= 'w', encoding='utf-8')

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
        
    def comment_parser(self, response):
        comments = response.css('div.el-card__body >div.layout-v')
        for comment in comments:
            company_slug = response.url.split(self.base_url)[1]
            url = comment.css('div.header >div.layout-h >h3.title >a::attr(href)').extract_first()
            yield SplashRequest(url =response.urljoin(url), callback= self.proscons_parser, meta={'company_slug':company_slug} )

    def proscons_parser(self, response):
        company = response.css('div.details >h1::text').extract()
        company_slug = [response.meta['company_slug']]
        url = [response.url]
        pros = response.css('div.pros >div.items >span.el-tag::text').extract()
        cons = response.css('div.cons >div.items >span.el-tag::text').extract()
        title = response.css('h3.title >a::text').extract()
        description= response.css('div.description-te>p::text').extract()
        tell_friend = ['NaN']
        rating = response.css('div.extra-info >div.mt-20 >div.rates-wrap >div.layout-h >div.ltr >div.el-rate ::attr(aria-valuenow)').extract()
        mean_salary = response.css('div.money-box >div.amount >strong.ml-5 ::text').extract()
        mean_salary = list(map(lambda x:x.splitlines()[1].replace('    ',''),mean_salary))
        like_count = response.css('div.footer >div.right-side >div.wrap-like >div.vote >div.like >span.count::text').extract()
        dislike_count = response.css('div.footer >div.right-side >div.wrap-like >div.vote >div.dislike >span.count::text').extract()

        if len(title)==0:
            title = ['NaN']
        if len(description)>1:
            description = [' '.join(description)]
        elif len(description) ==0:
            description = ['NaN']
 
        if len(company)==0:
            company = response.css('div.details >h2::text').extract()
        
        if len(pros) >0:
            pros = list(map(lambda x:x.splitlines()[1].replace('    ',''),pros))
        if len(cons)>0:
            cons = list(map(lambda x:x.splitlines()[1].replace('    ',''),cons))
        
        if len(pros) == 0:
            pros = ['NaN']

        if len(cons) == 0:
            pros = ['NaN']
        
        

        if len(rating) >3 :
            # rating_dict = {
            #     'mean_r' : [rating[0]],
            #     'life_work_balance' :[ rating[1]],
            #     'salary' : [rating[2]],
            #     'job_security' : [rating[3]],
            #     'managing' : [rating[4]],
            #     'work_culture' : [rating[5]],
            #     'type' : ['review'],
            # }
            rating_dict = {
                'f1' : [rating[0]],
                'f2' :[ rating[1]],
                'f3' : [rating[2]],
                'f4' : [rating[3]],
                'f5' : [rating[4]],
                'f6' : [rating[5]],
                'type' : ['review'],
            }
            tell_friend = response.css('div.extra-info >div.item >div.layout-h >span.el-tag::text').extract()
            tell_friend = list(map(lambda x:x.splitlines()[1].replace('    ',''),tell_friend))
        elif len(rating) == 2:
            rating_dict = {
                'f1' : [rating[0]],
                'f2' : [rating[1]],
                'f3':['NaN'],
                'f4':['NaN'],
                'f5':['NaN'],
                'f6':['NaN'],
                'type' : ['interview'],
            }
            # rating_dict{
            #     'interviewer'
            #     'company'
            # }
        self.log('=====================company: {},company_slug:{}, url :{}, pros:{}, cons:{}, title:{}, desc:{},like:{}, dislike:{}'.format(len(company), len(company_slug), len(url), len(pros), len(cons),len(title), len(description), len(like_count), len(dislike_count)))
        item = {
            'company_slug' : company_slug,
            'company' : company,
            'title' : title,
            'pros' :[pros],
            'cons' : [cons],
            'mean_salary':mean_salary,
            'comment' :list(description),
            'url' : url,
            'tell_friend' :tell_friend,
            'like' : [like_count],
            'dislike' : [dislike_count],
        }
        item.update(rating_dict)
        dataframe= pd.DataFrame(item)
        dataframe.to_csv('jobguy_pros_cons.csv', mode= 'a', encoding='utf-8', header=False)

    

