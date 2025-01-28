import scrapy
from itemloaders.processors import TakeFirst, MapCompose


def _default_na(value):
    value = value.strip() if isinstance(value, str) else value
    return value if value else "N/A"


class TakeFirstWithDefault(TakeFirst):
    def __call__(self, values):
        return super().__call__(values) or "N/A"


class OtomotoItem(scrapy.Item):
    model = scrapy.Field(output_processor=TakeFirstWithDefault())
    name = scrapy.Field(input_processor=MapCompose(_default_na), output_processor=TakeFirstWithDefault())
    users_data = scrapy.Field(input_processor=MapCompose(_default_na), output_processor=TakeFirstWithDefault())
    mileage = scrapy.Field(input_processor=MapCompose(_default_na), output_processor=TakeFirstWithDefault())
    fuel_type = scrapy.Field(input_processor=MapCompose(_default_na), output_processor=TakeFirstWithDefault())
    gearbox = scrapy.Field(input_processor=MapCompose(_default_na), output_processor=TakeFirstWithDefault())
    year = scrapy.Field(input_processor=MapCompose(_default_na), output_processor=TakeFirstWithDefault())
    place = scrapy.Field(input_processor=MapCompose(_default_na), output_processor=TakeFirstWithDefault())
    seller_type = scrapy.Field(input_processor=MapCompose(_default_na), output_processor=TakeFirstWithDefault())
    price = scrapy.Field(input_processor=MapCompose(_default_na), output_processor=TakeFirstWithDefault())


class OtomotoItem2(scrapy.Item):
    model = scrapy.Field()
    name = scrapy.Field()
    users_data = scrapy.Field()
    mileage = scrapy.Field()
    fuel_type = scrapy.Field()
    gearbox = scrapy.Field()
    year = scrapy.Field()
    place = scrapy.Field()
    seller_type = scrapy.Field()
    price = scrapy.Field()
