import time
import scrapy
from urllib.parse import urlparse
from ..items import BookItem


class ExtractData(scrapy.Spider):
    """
    Spider to extract book information from Booktopia.
    """
    name = "extract"
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.baseDomain = ""  # To store the base domain for relative URLs

    def start_requests(self):
        """
        Initiates requests to start URLs.
        """
        urls = ['https://www.booktopia.com.au/',]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        Parses the main page to extract category links.
        """
        parsed_url = urlparse(response.url)
        self.baseDomain = parsed_url.netloc  # Extract the base domain

        links = response.css('a')  # Get all anchor tags
        category_list = ('Fiction', 'Biographies & True Stories', 'Cooking, Food & Drink')  # Desired categories
        urls = {}  # Dictionary to store category URLs

        for link in links:
            category = link.css('::text').extract_first()  # Extract link text
            if category in category_list and category not in urls:
                # If the link text is a desired category and not already in the dictionary
                urls[category] = f"{self.baseDomain}{link.css('::attr(href)').extract_first()}"

        for category, url in urls.items():
            # Create the complete URL with sorter query parameter
            scrap_url = f'https://{url}?sorter=sortorder-en-dsc'
            yield scrapy.Request(scrap_url, callback=self.get_products_link, meta={'category': category})

    def get_products_link(self, response):
        """
        Parses the category page to extract product links.
        """
        category = response.meta['category']
        # Extract product links from the page
        product_links = response.xpath('//*[@id="product-results-p1"]/li/div[2]/div[2]/div/a/@href').extract()

        for link in product_links:
            # Create the complete product link
            product_link = f'https://{self.baseDomain}{link}'
            yield scrapy.Request(product_link, callback=self.scrap_product, meta={'category': category})

    def scrap_product(self, response):
        """
        Extracts product details from the product page.
        """
        time.sleep(1)  # Delay to avoid hitting the server too hard

        # Extract the required fields using XPath
        title = response.xpath('//*[@id="ProductDetails_d-product-info__rehyy"]/div/h1/text()').extract_first()
        author = response.xpath('//*[@id="ProductDetails_d-product-info__rehyy"]/div/p[1]/a/span/text()').extract_first()
        data = response.xpath('//*[@id="ProductDetails_d-product-info__rehyy"]/div/p[2]/text()').extract_first()
        data = data.split('|') if data is not None else ['','']
        published_date = data[1].strip() if len(data) > 1 else ''
        book_type = data[0].strip() if len(data) > 0 else ''
        original_price = response.xpath('//*[@id="BuyBox_product-version__uw1et"]/div[1]/div/div/div/p/span/text()').extract_first()
        discounted_price = response.xpath('//*[@id="BuyBox_product-version__uw1et"]/div[1]/div/div/p/text()').extract_first()
        publisher = response.xpath('//*[@id="ProductDetails_d-product-info__rehyy"]/div/div/h5/text()').extract_first()
        page_number = response.xpath('//*[@id="ProductDetails_d-product-info__rehyy"]/div/div/div/div[2]/div/div[1]/text()[2]').extract_first()
        category = response.meta['category']

        # Create an item to yield
        item = BookItem(
            title=title,
            author=author,
            published_date=published_date,
            book_type=book_type,
            original_price=original_price,
            discounted_price=discounted_price,
            publisher=publisher,
            page_number=page_number,
            category=category
        )
        yield item

    def __del__(self):
        """
        Destructor to clean up resources.
        """
        pass
