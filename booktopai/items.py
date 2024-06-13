import scrapy


class BookItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    published_date = scrapy.Field()
    book_type = scrapy.Field()
    original_price = scrapy.Field()
    discounted_price = scrapy.Field()
    publisher = scrapy.Field()
    page_number = scrapy.Field()
    category = scrapy.Field()
