import scrapy
import json
import pandas as pd

class CompanySalarySpider(scrapy.Spider):
    name = 'company_salary'
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
                item = {
                    'company_slug' : [company['company_slug']],
                    'company_name' : [company['name']],
                    'total_interview' : [company['total_interview']],
                    'total_companyreview' : [company['total_companyreview']],
                    'salary_min': [company['salary_min']],
                    'salary_max' : [company['salary_max']],
                    'over_all_rate' : [company['over_all_rate']],
                    'view_count' : [company['view_count']],
                    'company_link' : ['https://jobguy.ir/company/' + company['company_slug']],
                }
                item = pd.DataFrame(item)
                item.to_csv('jobguy_company_review.csv', mode= 'a', encoding='utf-8', header=False)
            yield scrapy.Request(url = self.urls.format(self.index), callback=self.parse)
