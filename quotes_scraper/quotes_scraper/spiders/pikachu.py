import scrapy
from ..items import QuotesScraperItem

class PikachuSpider(scrapy.Spider):
    name="pikachu"
    start_urls=[
        'https://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        items = QuotesScraperItem()

        all_div_quotes = response.css('div.quote')

        for quotes in all_div_quotes:
            text = quotes.css('span.text::text').extract_first()
            author = quotes.css('span small.author::text').extract_first()
            tags = quotes.css('div.tags a.tag::text').extract()

            items['text'] = text
            items['author'] = author
            items['tags'] = tags

            yield items

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)