# -*- coding: utf-8 -*-

# Scrapy settings for huya project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'huya'

SPIDER_MODULES = ['huya.spiders']
NEWSPIDER_MODULE = 'huya.spiders'

# ITEM_PIPELINES = {'huya.pipelines.HuyaPipeline':100}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'huya (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True
ROBOTSTXT_OBEY = False

FEED_URI = 'file:G://Program/Projects/Live_Sipder/huya/test.csv'
FEED_FORMAT = 'csv'

FIELDS_TO_EXPORT = [
    'topic_url',
    'room_url'
]

COOKIES ="{'__yamid_tt1': '0.5512255863552324', '__yamid_new': 'C7EC370DD7600001F4C11580B55012AE', 'SoundValue': '0.50', 'guid': '0e74abbb3bffb65a032cc646c7468f6b', 'UM_distinctid': '1625ad4fcd320c-0bef0a9a4647eb-50683974-13c680-1625ad4fcd425a', 'CNZZDATA1266840534': '225127450-1521937827-%7C1521937827', 'isInLiveRoom': '', 'Hm_lvt_51700b6c722f5bb4cf39906a596ea41f': '1522544539,1522625547,1523670647,1523700046', '__yasmid': '0.5512255863552324', 'udb_passdata': '2', 'udb_guiddata': 'ca0e69762f8f4757870c11bd0770f62a', 'ya_eid': 'navi/sign', 'udb_accdata': '13250219510', 'h_unt': '1523724897', 'PHPSESSID': 'vpmp96dui8f6a3s9b92i8jq8t2', 'Hm_lpvt_51700b6c722f5bb4cf39906a596ea41f': '1523724987', '__yaoldyyuid': '', '_yasids': '__rootsid%3DC7F2DC3D0220000184131600160823D0', 'udb_uid': '2232479408', 'yyuid': '2232479408', 'udb_passport': '2232684128yy', 'udb_version': '1.0', 'udb_biztoken': 'AQCx-CxLwJte5z6O7LaVw6b7DOH4HylviLJiEg4dvk7Po1TXsbyfc-4IQVpX2NQDsdd1wp0ulYKn8JZqxdE4xqi-ROAdPHcepNFwvV0jylBhXT2jx1vGMhTwPNmMXiWVTmxfQ7QM7F4neRCr9owxDMqLvoSmjpp1J-YvDbRgy6nlmmhbEuRVd6Pqgh1FuBYZdU4uCOtZjwFeGrqcafrKhcw0bxpZCg-ybJPQVUohQbpU2244GeDCMGYBEIKB9tX0xtPn1J_419m_SCyoTyx07PINB7_YB4Hcvydqiss7f4413SeNLzi5gW9wt5F5vB808YKkisH_8NiqjFsuLUH_Q4_j', 'udb_origin': '100', 'udb_other': '%7B%22lt%22%3A%221523725018269%22%2C%22isRem%22%3A%221%22%7D', 'username': '2232684128yy', 'password': '8396429B8622AFFCD6B526630E591C16F477DFC8', 'osinfo': '3AE360BF02A8CFD8D336BB0F81F45A7627349660', 'udb_l': 'DAAyMjMyNjg0MTI4eXnaMtJaBlQA4XOT_hNEo_Umf-ZFyosxBpUjax2kJH7q7eykyynHiSjq70WHIV2bI7oq47hgyTV56YX1fPSJLEMefSE7DR99P2BB0SjtVzB0SalVKLZmxDGncTI5AAAAAAMAAAAAAAAADQAxMTMuNjUuNzAuMTEyBAA1OTEz', 'udb_n': 'D0FD74EF8406A550FE6D12710FE32029507E16AB271B6B4CB0BC19933EFF3E5E', 'udb_oar': '7EC0A6304ACD8C45A535C9B5352784E39A7CC71D4110C764594A89E116B3BE1A060BB5EA3F9EB3287FFD9E810DF718C3EA34988F3A15092CDCDDC7CAD352E07A69570C13D6D36E29B30D296260C2C0077835743616DB9298F24FAE5D0B4D612EC0EF09EBA35DBF07E8924B46A709FF68956479F5F8FDB8F7302C968BF3C36928053FEF185A80643D854A147DF3CA92326138F55D3BDC89A4E180C3D1F0146B9DD9C0751344D36A495639423EE9E981FFD183E9B8A5529F1AF4A23AF5F4C4F814269DF47F4496C9825F5A32E6C399ECB27A1611BFBDEDEE35F408D7407234F15500302658F5CD66C3625564D807FD2840FDD03635282130C9C9CAB6DABB08F3A62FE79146AC8FFCE45AEE22B6870D8FA536E0C4D056217E554943DA4213E780ECEB654319E39FB9145B05D39B3F5F249F8034C4CB4ADE95E11F3E850BF5B3464F"
COOKIES_DEBUG = True
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'
}


# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'huya.middlewares.HuyaSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'huya.middlewares.MyCustomDownloaderMiddleware': 543,
   'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': 700
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'huya.pipelines.HuyaPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

LOG_LEVEL = 'INFO'

# Mongodb Configuration
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT =  27017
MONGODB_DB_NAME = 'huya'
MONGODB_USER_NAME = None
MONGODB_PASSWORD = None
