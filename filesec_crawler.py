import scrapy

class FilesecSpider(scrapy.Spider):
    name = 'filesec'
    start_urls = ['https://filesec.io/']

    def parse(self, response):
        for ext in response.css('tr.extension-row'):
            next_page = ext.xpath('td/a/@href').get()
            yield response.follow(next_page, self.parse_page)

    def parse_page(self, response):
        desc = response.css('div.description::text').getall()
        # js page buggy
        try:
            recommendation = desc[1]
            description = desc[0]
            extension = response.css('div.extension-title h1::text').re(r'[a-zA-Z0-9.]+')[0]
            ressources = response.css('a.link::text').getall()
            yield {"extension":extension,
                   "description":description,
                   "recomendation":recommendation,
                   "ressources":ressources}
        except IndexError:
            pass
