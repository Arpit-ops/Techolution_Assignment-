import os
import csv

class CsvPipeline:
    def open_spider(self, spider):
        # Ensure the directory exists
        os.makedirs('output', exist_ok=True)

        # Open the CSV file
        self.file = open('output/books.csv', 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['Title', 'Author', 'Published Date', 'Book Type', 'Original Price', 'Discounted Price', 'Publisher', 'Page Number', 'Category'])

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.writer.writerow([
            item['title'],
            item['author'],
            item['published_date'],
            item['book_type'],
            item['original_price'],
            item['discounted_price'],
            item['publisher'],
            item['page_number'],
            item['category']
        ])
        return item
