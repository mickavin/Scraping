from api.utils import get_random_agent
import os 
# Scrapy settings for api project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'api'

SPIDER_MODULES = ['api.spiders']
NEWSPIDER_MODULE = 'api.spiders'
SPLASH_URL = 'https://mbxardqk-splash.scrapinghub.com'

FEED_EXPORT_ENCODING = 'utf-8'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'api (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DOWNLOADER_MIDDLEWARES = {
#    'projectname.middlewares.CustomMiddleware': 543,
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'api.middlewares.ApiSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 610,
    'scrapy_requests.RequestsMiddleware': 800,
    'api.middlewares.ApiSpiderMiddleware': 200,
    'scrapy_crawlera.CrawleraMiddleware': 610
}

# enable Zyte Proxy
ZYTE_SMARTPROXY_ENABLED = True

# settings Zyte
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

CRAWLERA_ENABLED = True

ZYTE_SMARTPROXY_PRESERVE_DELAY = 600
ZYTE_SMARTPROXY_URL = 'http://proxy.zyte.com:8010'
AUTOTHROTTLE_ENABLED = True
CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_DOMAIN = 32
DOWNLOAD_TIMEOUT = 600 
USER_AGENT = get_random_agent()

CRAWLERA_PRESERVE_DELAY = True
# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'api.pipelines.ApiPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings

# the APIkey you get with your subscription
ZYTE_SMARTPROXY_APIKEY = 'YOUR_ZYTE_SMARTPROXY_APIKEY'
CRAWLERA_APIKEY = 'YOUR_CRAWLERA_APIKEY'
ZYTE_APIKEY = 'YOUR_ZYTE_APIKEY'
SPLASH_APIKEY = 'YOUR_SPLASH_APIKEY'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'