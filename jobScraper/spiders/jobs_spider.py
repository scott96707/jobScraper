import scrapy


class JobsSpider(scrapy.Spider):
    name = "jobs"
    start_urls = [
        'https://www.wuxiaworld.com/novel/martial-world/mw-chapter-1376'
    ]

    def parse(self, response):
        for chapter in response.css('div.fr-view'):
            yield {
                    'title': chapter.xpath("//meta[@name='description']/@content").extract(),
                    'body': chapter.xpath("//div[@class='fr-view']/p/*/text()").extract(),
            }
        
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
