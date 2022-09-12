import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest, SplashJsonResponse, SplashTextResponse
from scrapy.http import HtmlResponse
from pkgutil import get_data
from api.utils import get_random_agent
from w3lib.http import basic_auth_header

USER_AGENT = get_random_agent()

class CrawleventsSpider(CrawlSpider):
    name = 'crawlevents'
    allowed_domains = ['ticketmaster.fr']
    start_urls = ['https://www.ticketmaster.fr/fr/rechercheavancee']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=['//div[@class="resultat-vide-prop-first"]/ul/li/a']), callback='parse_item', process_request="use_splash"),
    )

    http_user = '7f4f49d98cbe4bd8a6fd1fa8ff05b39a'
    http_pass = ''

    def __init__(self, *args, **kwargs):
            # to be able to load the Lua script on Scrapy Cloud, make sure your
            # project's setup.py file contains the "package_data" setting, similar
            # to this project's setup.py
            self.LUA_INIT = get_data(
                'api', 'scripts/init.lua'
            ).decode('utf-8')
            self.LUA_NEXT = get_data(
                'api', 'scripts/next.lua'
            ).decode('utf-8')
            super(CrawleventsSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url, 
                args={
                    'wait': 3,
                    'lua_source': self.LUA_INIT,
                    'timeout': 60,
                    'images': 0, 
                    'resource_timeout': 10,
                    "har": 0, 
                    "png": 0
                    },  
                splash_headers={
                    'Authorization': basic_auth_header(self.settings['SPLASH_APIKEY'], ''),
                },
                headers={
                    #'User-Agent': USER_AGENT,
                    'crawlera_user': self.settings['CRAWLERA_APIKEY'],
                    }
                )

    def use_splash(self, request):
        request.meta['splash'] = {
                'endpoint':'render.html',
                'args':{
                    'wait': 5,
                    }
                }
        return request

    def _requests_to_follow(self, response):
        if not isinstance(
                response,
                (HtmlResponse, SplashJsonResponse, SplashTextResponse)):
            return
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                yield rule.process_request(r)

    def parse_address(self, response, item):
        address = response.xpath('//dd[@itemprop="address"]/ul/li/span/text()').get()
        postal_code = response.xpath('//dd[@itemprop="address"]/ul/li[2]/span[@itemprop="postalCode"]/text()').get()
        locality = response.xpath('//dd[@itemprop="address"]/ul/li[2]/span[@itemprop="addressLocality"]/text()').get()
       
        yield {
            'item': item,
            'address': {
                'address': address,
                'postal_code': postal_code,
                'locality': locality,
        }}

    def parse_item(self, response):
        blocs = response.xpath('//article[@class="bloc-result bloc-billet-fr"]')
        for bloc in blocs:
            link = bloc.xpath('.//a/@href').get()
            image = bloc.xpath('.//a/img/@src').get()
            start_date = bloc.xpath('.//div/div/p[@class="bloc-result-when"]/time[@itemprop="startDate"]/@content').get()
            end_date = bloc.xpath('.//div/div/p[@class="bloc-result-when"]/time/meta[@itemprop="endDate"]/@content').get()
            place = bloc.xpath('.//div[@class="bloc-result-content"]/div[@class="bloc-result-details"]/div[@class="bloc-result-content-details"]/div[@class="bloc-result-infos"]/p/a/@title').get()
            city = bloc.xpath('.//div[@class="bloc-result-content"]/div[@class="bloc-result-details"]/div[@class="bloc-result-content-details"]/div[@class="bloc-result-infos"]/p/a/span[@itemprop="address"]/span/text()').get()
            price =  bloc.xpath('normalize-space(.//div/div/div[@class="bloc-result-ticket-info"]/p[@class="bloc-result-price"]/strong/text())').get()
            type = bloc.xpath('normalize-space(.//div[@class="bloc-result-content"]/div[@class="bloc-result-details"]/div[@class="bloc-result-content-details"]/div[@class="bloc-result-infos"]/p[@class="bloc-result-type"]/text())').get()
            artist =  bloc.xpath('.//div[@class="bloc-result-content"]/div[@class="bloc-result-details"]/div[@class="bloc-result-content-details"]/div[@class="bloc-result-infos"]/p[contains(@class, "bloc-result-artist")]/a/text()').get()
            item={}
            if end_date:
                item = {
                    'link': link,
                    'image': image,
                    'start_date': start_date,
                    'end_date': end_date,
                    'place': place,
                    'city': city,
                    'price': price,
                    'type': type,
                    'artist': artist,
                    'merchant': "Ticketmaster",
                }
            else:
                item = {
                    'link': link,
                    'image': image,
                    'start_date': start_date,
                    'place': place,
                    'city': city,
                    'price': price,
                    'type': type,
                    'artist': artist,
                    'merchant': "Ticketmaster"
                }
            yield response.follow(link, callback=self.parse_address, cb_kwargs=dict(item=item))
        next = response.xpath("//a[@title='Page suivante'][@onmousedown]")
        if next:
            le = LinkExtractor()
            for link in le.extract_links(response):
                yield SplashRequest(
                    link.url,
                    self.parse_item,
                    endpoint='render.json',
                    #headers={'User-Agent': USER_AGENT},
                    args={
                        'html': 1,
                        'lua_source': self.LUA_NEXT,
                        'crawlera_user': self.settings['CRAWLERA_APIKEY'],
                        'timeout': 60,
                        'images': 0, 
                        'resource_timeout': 10,
                        "har": 0, 
                        "png": 0
                    },
                    splash_headers={
                    'Authorization': basic_auth_header(self.settings['SPLASH_APIKEY'], ''),
                    },     
                    #cache_args=['lua_source'],

                )
            