from typing import Any, Iterable
import scrapy
from isapi.samples.redirector import proxy
from scrapy.crawler import CrawlerProcess
from scrapy.http import Response
from scrapy.loader import ItemLoader
from SubClasses import OtomotoItem
import random

class OtoMotoSpider(scrapy.Spider):
    name = 'OtoMotoSpider'
    base_url = 'https://www.otomoto.pl/osobowe/{model}?page={page_number}'
    car_models = ['Abarth', 'Acura', 'Aiways', 'Aixam', 'Alfa Romeo', 'Alpine', 'Arcfox', 'Asia', 'Aston Martin',
                  'Audi', 'Austin', 'Autobianchi', 'AVATR', 'Baic', 'Bentley', 'BMW', 'BMW-ALPINA', 'Brilliance',
                  'Bugatti', 'Buick', 'BYD', 'Cadillac', 'Casalini', 'Caterham', 'Cenntro', 'Changan', 'Chatenet',
                  'Chevrolet', 'Chrysler', 'Citroën', 'Cupra', 'Dacia', 'Daewoo', 'Daihatsu', 'DeLorean', 'DFM',
                  'DFSK', 'DKW', 'Dodge', 'Doosan', 'DR MOTOR', 'DS Automobiles', 'e.GO', 'Elaris', 'FAW', 'FENDT',
                  'Ferrari', 'Fiat', 'Fisker', 'Ford', 'Forthing', 'Gaz', 'Geely', 'Genesis', 'GMC', 'GWM', 'HiPhi',
                  'Honda', 'Hongqi', 'Hummer', 'Hyundai', 'iamelectric', 'Ineos', 'Infiniti', 'Inny', 'Isuzu', 'Iveco',
                  'JAC', 'Jaecoo', 'Jaguar', 'Jeep', 'Jetour', 'Jinpeng', 'Kia', 'KTM', 'Lada', 'Lamborghini', 'Lancia',
                  'Land Rover', 'Leapmotor', 'LEVC', 'Lexus', 'Ligier', 'Lincoln', 'Lixiang', 'Lotus', 'LTI', 'Lucid',
                  'Lynk &amp; Co', 'MAN', 'Maserati', 'MAXIMUS', 'Maxus', 'Maybach', 'Mazda', 'McLaren', 'Mercedes-Benz',
                  'Mercury', 'MG', 'Microcar', 'MINI', 'Mitsubishi', 'Morgan', 'NIO', 'Nissan', 'Nysa', 'Oldsmobile',
                  'Omoda', 'Opel', 'Peugeot', 'Piaggio', 'Plymouth', 'Polestar', 'Polonez', 'Pontiac', 'Porsche', 'RAM',
                  'Renault', 'Rolls-Royce', 'Rover', 'Saab', 'SARINI', 'Saturn', 'Seat', 'Seres', 'Shuanghuan', 'Skoda',
                  'Skywell', 'Skyworth', 'Smart', 'SsangYong', 'Subaru', 'Suzuki', 'Syrena', 'Tarpan', 'Tata', 'Tesla',
                  'Toyota', 'Trabant', 'Triumph', 'Uaz', 'Vauxhall', 'VELEX', 'Volkswagen', 'Volvo', 'Voyah', 'WALTRA',
                  'Warszawa', 'Wartburg', 'Wołga', 'Xiaomi', 'XPeng', 'Zaporożec', 'Zastava', 'ZEEKR', 'Zhidou', 'Żuk']

    proxies = [
        'http://173.212.227.160:21025',
        'http://185.109.184.150:49217',
        'http://77.93.220.70:61556',
        'http://185.132.178.143:1080',
        'http://185.217.51.10:4444',
        'http://213.135.234.101:4153',
        'http://5.135.136.19:12321',
        'http://46.227.37.73:51155',
    ]

    def start_requests(self) -> Iterable[scrapy.Request]:
        for model in self.car_models:
            url = self.base_url.format(model=model, page_number=1)
            yield scrapy.Request(url=url, callback=self.parse, meta={'model': model, 'page_number': 1})

    def parse(self, response: Response, **kwargs: Any) -> Any:
        model = response.meta['model']
        page= response.meta['page_number']

        listings = response.xpath('//article[@class="ooa-1yux8sr e1wxlbcc0"]')

        for listing in listings:
            yield self._parse_items(listing, model)

        next_page = response.xpath('//li[@title="Next Page"]/@href').get()
        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse,
                meta={'model': model,
                      'page_number': page + 1,
                      'proxy': random.choice(self.proxies)}
            )

    @staticmethod
    def _parse_items(listing, model) -> OtomotoItem:
        loader = ItemLoader(item=OtomotoItem(), selector=listing)
        loader.add_value('model', model)
        loader.add_xpath('name', './/h2/a/text()')
        loader.add_xpath('users_data', './/p[contains(@class, "ewg8vos8 ooa-1tku07r")]/text()')
        loader.add_xpath('mileage', './/dd[@data-parameter="mileage"]/text()')
        loader.add_xpath('fuel_type', './/dd[@data-parameter="fuel_type"]/text()')
        loader.add_xpath('gearbox', './/dd[@data-parameter="gearbox"]/text()')
        loader.add_xpath('year', './/dd[@data-parameter="year"]/text()')
        loader.add_xpath('place', './/p[contains(@class, "ooa-oj1jk2")]/text()')
        loader.add_xpath('seller_type', './/li[contains(@class, "ooa-1y6ajhy ebwza7n5")]/text()')
        loader.add_xpath('price', './/h3[contains(@class, "e6r213i1 ooa-1n2paoq")]/text()')
        return loader.load_item()

process = CrawlerProcess(settings={
    "FEEDS": {
        "output_otomotoBest.csv": {"format": "csv"},
    },
    "USER_AGENT": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/117.0.5938.92 Safari/537.36"),
    "LOG_LEVEL": "INFO",
    "HTTPCACHE_ENABLED": False,
    "DOWNLOAD_DELAY": 1,
    "RANDOMIZE_DOWNLOAD_DELAY": True,
    "ROBOTSTXT_OBEY": False,
})

process.crawl(OtoMotoSpider)
process.start()