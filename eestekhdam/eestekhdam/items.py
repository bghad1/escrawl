import scrapy


class EestekhdamItem(scrapy.Item):
    position_url = scrapy.Field()
    position = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    pass
