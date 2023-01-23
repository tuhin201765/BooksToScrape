import scrapy
from ..items import BooksItem


class BookSpider(scrapy.Spider):
    name = 'book'
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        links = response.css('.product_pod a::attr(href)').getall()
        for link in links:
            yield response.follow(link, self.parse_link)
            # link = response.urljoin(link)
            # yield scrapy.Request(link,callback=self.parse_link)
        next_page = response.css('.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
            # next_page = response.urljoin(next_page)
            # yield scrapy.Request(next_page,callback=self.parse)
    def parse_link(self, response):
        item = BooksItem()
        item['title'] = response.css('h1::text').get().strip()
        item['price'] = response.css('.product_main .price_color::text').get().strip()
        item['description'] = response.css('#product_description+ p::text').get().strip()
        yield item
