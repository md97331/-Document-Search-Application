import scrapy
import os
import urllib.parse

class WikipediaSpider(scrapy.Spider):
    # Spider name used to run the spider from the command line
    name = 'wiki_spider'
    # Domains allowed to be scraped to avoid crawling external sites!!!
    allowed_domains = ['en.wikipedia.org']
    # Starting URL for the crawl; this is our entry point
    start_urls = ['https://en.wikipedia.org/wiki/Technology', 
                  'https://en.wikipedia.org/wiki/John_Cena',
                  'https://en.wikipedia.org/wiki/World_War_II']

    # Custom settings for the spider to control crawl behaviour
    custom_settings = {
        # Limit requests to 3 per domain to avoid overloading servers
        'CONCURRENT_REQUESTS_PER_DOMAIN': 3,
        # Depth limit restricts how far the spider will go from the initial page
        'DEPTH_LIMIT': 2,
        # Maximum number of concurrent requests performed by the spider
        'CONCURRENT_REQUESTS': 16
    }

    # Page counter to keep track of how many pages have been crawled
    page_count = 0  
    # Maximum number of pages to scrape to avoid excessively large crawls
    max_pages = 500
    
    def parse(self, response):
        # Folder where the scraped HTML files will be saved
        domain_folder = './[FLASK] main/docs'
        # Create the folder if it doesn't already exist
        if not os.path.exists(domain_folder):
            os.makedirs(domain_folder)

        # Check if the page count is less than the maximum allowed
        if self.page_count < self.max_pages:
            # Only process pages from 'en.wikipedia.org'
            if 'en.wikipedia.org' in response.url:
                # Extract relevant information from the page using CSS selectors
                title = response.css('h1#firstHeading::text').get()
                headings = response.css('div.mw-parser-output h2 span.mw-headline::text').getall()
                body_text = response.css('div.mw-parser-output p::text').getall()
                categories = response.css('div#mw-normal-catlinks a::text').getall()
                last_edit_info = response.css('li#footer-info-lastmod::text').get()
                
                # Generate a clean filename from the URL to save the page
                filename = clean_filename(response.url.split("/")[-1]) + '.html'

                # Avoid saving files with certain prefixes that are typically non-articles
                if not any(filename.startswith(prefix) for prefix in ('File:', 'Category:')):
                    filepath = os.path.join(domain_folder, filename)
                    with open(filepath, 'wb') as f:
                        f.write(response.body)

                # Increment the page count after saving a page
                self.page_count += 1  

                # Yield the extracted information, making it available for further processing
                yield {
                    'url': response.url,
                    'title': title,
                    'headings': headings,
                    'body_text': body_text,
                    'categories': categories,
                    'last_edit_info': last_edit_info
                }

                # Follow links within Wikipedia to continue crawling
            for link in response.css('div.mw-parser-output a::attr(href)').getall():
                next_page = response.urljoin(link)
                # Only follow the link if the max_pages limit has not been reached
                if self.page_count < self.max_pages:
                    yield scrapy.Request(next_page, callback=self.parse)
                else:
                    self.logger.info("MAX PAGE LIMIT REACHED")

# Helper function to create a clean filename from a Wikipedia article title
def clean_filename(filename):
    # Split the filename by '/' and decode URL-encoded characters
    components = filename.split('/')
    decoded_components = [urllib.parse.unquote(part) for part in components]
    # Rejoin the components to form the cleaned filename
    return '/'.join(decoded_components)
