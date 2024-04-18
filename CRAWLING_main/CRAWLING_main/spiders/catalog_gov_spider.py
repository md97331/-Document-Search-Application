import scrapy
import os

class DataCatalogSpider(scrapy.Spider):
    name = "datacatalog_spider"
    start_urls = [
            'https://catalog.data.gov/dataset/?groups=climate5434',
            'https://catalog.data.gov/dataset/?vocab_category_all=Human+Health',
            'https://catalog.data.gov/dataset/?vocab_category_all=Transportation',
            'https://catalog.data.gov/dataset/?vocab_category_all=Ecosystem+Vulnerability'
    ]

    def parse(self, response):
        for dataset_link in response.css('h3.dataset-heading a::attr(href)').getall():
            yield response.follow(dataset_link, callback=self.save_dataset)

    def save_dataset(self, response):
        
        # Extract title
        title_element = response.xpath('/html/body/div[2]/div/div[2]/div/article/section[1]/h1')
        title = title_element.xpath('.//text()').get().strip() if title_element else None

        # Extract description
        description_element = response.xpath('/html/body/div[2]/div/div[2]/div/article/section[1]/div[2]/p')
        description = description_element.xpath('.//text()').get().strip() if description_element else None

        # Generate filename and save HTML
        if title:
            filename = f"{title}.html"
            filepath = '/Users/mariodiaz/Desktop/CS429/PROJ/[FLASK] main/docs/' + filename
            
            with open(filepath, 'wb') as f:
                f.write(response.body) 
        else:
            print(f"Warning: Title not found for {response.url}")
