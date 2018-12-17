import scrapy


class JobsSpider(scrapy.Spider):
    name = "jobs"
    start_urls = [
        "https://www.indeed.com/jobs?q=Python&l=Denver%2C+CO&sort=date",
    ]

    def parse(self, response):
        for posting in response.xpath('//div[@data-tn-component="organicJob"]'):
            yield {
                    'jobtitle': posting.xpath('//div[@data-tn-component="organicJob"]/h2[@class="jobtitle"]/a[@data-tn-element="jobTitle"]/text()').extract(),
                   # 'company': posting.xpath('//span[@class="company"]/a/text()').extract(),
                   # 'location': posting.xpath('//div[@class="location"]/text()').extract(),
            }
