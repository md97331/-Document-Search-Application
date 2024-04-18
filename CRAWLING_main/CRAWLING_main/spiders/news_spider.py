import scrapy
import os

class YahooNewsSpider(scrapy.Spider):
    name = 'yahoo_spider'
    allowed_domains = ['yahoo.com']
    start_urls = [
        'https://www.yahoo.com/news/us/',
        'https://www.yahoo.com/news/world/', 
        'https://www.yahoo.com/news/science/',
        'https://www.yahoo.com/news/local/',
        'https://www.yahoo.com/news/business/'
        'https://www.yahoo.com/news/sports/',
        'https://www.yahoo.com/news/entertainment/'

    ]

    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 4,
        'DEPTH_LIMIT': 2, 
        'CONCURRENT_REQUESTS':16
    }

    page_count = 0
    max_pages = 50

    def parse(self, response):

        if self.page_count < self.max_pages:
            if 'yahoo.com' in response.url:
                # Target Elements on the Yahoo News Article:
                title = response.css('h1::text').get()  
                author = response.css('span.caas-attr-meta-byline span::text').getall() 
                content = response.css('div.caas-body p::text').getall() 

                filename = title[:50] + '.html'
                filepath = '/Users/mariodiaz/Desktop/CS429/PROJ/[FLASK] main/docs/' + filename

                with open(filepath, 'wb') as f:
                    f.write(b"<html><head><title>" + title.encode('utf-8') + b"</title></head><body>")
                    if author:
                        f.write(b"<h1>" + " ".join(author).encode('utf-8') + b"</h1>") # Join author names if multiple
                    for p in content:
                        f.write(p.encode('utf-8'))
                    f.write(b"</body></html>")
                
                self.page_count += 1

                yield {
                    'url': response.url,
                    'title': title,
                    'author': author,
                    'content': content,
                }

            # Find links within Yahoo News (may need refining):
            for link in response.css('a[href^="/news/"]::attr(href)').getall(): 
                next_page = response.urljoin(link)
                if self.page_count < self.max_pages:
                    yield scrapy.Request(next_page, callback=self.parse)
                else:
                    self.logger.info("MAX PAGE LIMIT REACHED")
