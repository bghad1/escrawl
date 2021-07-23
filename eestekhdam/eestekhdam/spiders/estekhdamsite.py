import scrapy
from ..items import EestekhdamItem


def parse_attr(response):
    items = []
    position = response.css('h1.entry-title a::text').get()
    phone = response.css('div.contact-mobile span.contact-data a::text').get()
    email = response.css('div.contact-email span.contact-data a::text').get()
    item = EestekhdamItem()
    item["position_url"] = response.url
    item["position"] = position
    if phone:
        item["phone"] = phone
    else:
        item["phone"] = "بدون موبایل"
    if email:
        item["email"] = email
    else:
        item["email"] = "بدون ایمیل"
    items.append(item)
    yield dict(item)


class EstekhdamsiteSpider(scrapy.Spider):
    name = 'estekhdamsite'
    allowed_domains = ['e-estekhdam.com']
    start_urls = ['https://e-estekhdam.com/search?page=1']

    BASE_URL = 'https://e-estekhdam.com'

    def parse(self, response):
        # links = response.css('a.ee-left::attr(href)').getall()
        links = response.css('div.media-body a.title::attr(href)').getall()
        # links = response.css('a.col-xs-12 col-md-4 view hidden-sm hidden-xs::attr(href)').getall()
        for link in links:
            absolute_url = self.BASE_URL + link
            yield scrapy.Request(absolute_url, callback=parse_attr)

        next_page = response.xpath('.//a[@rel="next"]/@href').extract()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
        if next_page:
            next_href = next_page[0]
            next_page_url = self.BASE_URL + next_href
            # next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

# scrapy crawl estekhdam -o e-estekhdam.xlsx