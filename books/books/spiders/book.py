import scrapy


class BookSpider(scrapy.Spider):
    name = 'book'
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        links = response.css('.product_pod a::attr(href)').getall()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link,callback=self.parse_link)
        next_page = response.css('.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page,callback=self.parse)
    def parse_link(self,response):
        title = response.css('h1::text').get().strip()
        price = response.css('.product_main .price_color::text').get().strip()
        description = response.css('#product_description+ p::text').get().strip()
        yield {'Title':title,'Price':price,'Description':description}