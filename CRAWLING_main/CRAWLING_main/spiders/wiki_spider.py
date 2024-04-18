import scrapy
import os
import urllib.parse

class WikipediaSpider(scrapy.Spider):
    name = 'wiki_spider'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/bad_bunny']

    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 3,
        'DEPTH_LIMIT': 2,  # Adjust as needed
        'CONCURRENT_REQUESTS':  16
    }

    page_count = 0  
    max_pages = 500  # Set your desired maximum
    
    def parse(self, response):
        domain_folder = './[FLASK] main/docs'
        if not os.path.exists(domain_folder):
            os.makedirs(domain_folder)

        if self.page_count < self.max_pages:
            if 'en.wikipedia.org' in response.url:
                title = response.css('h1#firstHeading::text').get()
                headings = response.css('div.mw-parser-output h2 span.mw-headline::text').getall()
                body_text = response.css('div.mw-parser-output p::text').getall()
                categories = response.css('div#mw-normal-catlinks a::text').getall()
                last_edit_info = response.css('li#footer-info-lastmod::text').get()
                
                filename = clean_filename(response.url.split("/")[-1]) + '.html'

                if not any(filename.startswith(prefix) for prefix in ('File:', 'Category:')):
                    filepath = '/Users/mariodiaz/Desktop/CS429/PROJ/[FLASK] main/docs/' + filename
                    with open(filepath, 'wb') as f:
                        f.write(response.body)

                self.page_count += 1  # Only increment if saved

                yield {
                    'url': response.url,
                    'title': title,
                    'headings': headings,
                    'body_text': body_text,
                    'categories': categories,
                    'last_edit_info': last_edit_info
                }

                # Follow links within Wikipedia:
            for link in response.css('div.mw-parser-output a::attr(href)').getall():
                next_page = response.urljoin(link)
                if self.page_count < self.max_pages:  # Check if the max_pages limit is not reached before following
                    yield scrapy.Request(next_page, callback=self.parse)
                else:
                    self.logger.info("MAX PAGE LIMIT REACHED")

    
def clean_filename(filename):
            components = filename.split('/')
            decoded_components = [urllib.parse.unquote(part) for part in components]
            return '/'.join(decoded_components)