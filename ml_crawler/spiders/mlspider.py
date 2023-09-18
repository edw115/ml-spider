import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from ..items import MlCrawlerItem

class MLSpider(CrawlSpider):
    name = 'ml_crawler'
    allowed_domains = ['listado.mercadolibre.com.ve','articulo.mercadolibre.com.ve']
    start_urls = ['https://listado.mercadolibre.com.ve/impresoras']
    download_delay = 2

    rules=(
        #Pagination
        Rule(
            LinkExtractor(
                allow=r'/_Desde_'
            ),follow=True
        ),
        #Details page
        Rule(
            LinkExtractor(
                allow=r'/MLV-',
            ), follow=True, callback='parse_item'
        )
    )

    def clear_text(self, text):
        new_text = text.replace('\n','').replace('\r','').replace('\t','').strip()
        return new_text
    
    def parse_item(self,response):
        sel = Selector(response)
        item = ItemLoader(MlCrawlerItem(), sel)
        item.add_xpath('title','//h1/text()', MapCompose(self.clear_text))
        item.add_xpath('price','//meta[@itemprop="price"]/@content',MapCompose(self.clear_text))
        item.add_xpath('description','//*[contains(@class,"description__content")]/text()',MapCompose(self.clear_text))

        yield item.load_item()