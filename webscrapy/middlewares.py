# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals, Request
import random
from webscrapy.settings import USER_AGENT_LIST
from scrapy.exceptions import IgnoreRequest, NotConfigured

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

def get_cookies_dict():
    cookies_str = 'mm_visitor_id=5ca45b1d-a05b-4565-b24b-79e5d0cffcbe; didomi_token=eyJ1c2VyX2lkIjoiMTg4ZGQzNGQtNmYxYi02NWY2LTg2ZWEtZWMzZjI0NzgxY2FlIiwiY3JlYXRlZCI6IjIwMjMtMDYtMjFUMDk6MDc6MDYuNzgxWiIsInVwZGF0ZWQiOiIyMDIzLTA2LTIxVDA5OjA3OjA2Ljc4MVoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiYzp2ZW5kb3JuZWMtTGFjMkJXNEQiLCJjOnZlbmRvcnN0YS1hd2ZUVUNBUCIsImM6dmVuZG9ycHJlLWNGaVhEeEhLIiwiYzp2ZW5kb3JtYXItQUFHdFBBSGYiXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsic3RhdGlzdGljcyIsInVzZXJQcmVmZXJlbmNlcyIsInBlcnNvbmFsaXNlZEFkdmVydGlzaW5nIl19LCJ2ZXJzaW9uIjoyfQ==; euconsent-v2=CPttmcAPttmcAAHABBENDJCgAAAAAAAAAAqIAAAAAAAA.YAAAAAAAAAAA; _gcl_au=1.1.188159675.1687338427; mm_ab_test_version=240ad5c4fdad2262c1f4ba39a89228b0; mm_ab_tests=60.1|303.0|368.1|371.1|785.1|877.1|959.1|941.1|1016.1|1039.1|1043.1|1129.1|1146.1|1150.0|1151.1|1156.1|1157.1|1207.1|1215.1|1218.1|1228.1|1233.1|1243.1|1245.1|1205.1|1331.1|1355.1|1388.1|1389.0|1455.1|1457.0|1521.1|1522.1|1523.1|1524.0|1526.1|1533.0|1534.1|1553.1|1652.1|1686.0|1753.1|1759.0|1762.1|1765.1|1359.1|1786.1|1916.1|1983.1|1984.1|1985.1|1986.1|2015.1|2048.1|2180.1|2312.0|2345.1|2412.1|2511.1|2513.1|2544.1|2643.1|2675.1|2676.1|2708.0|2807.1|2843.0|2906.1|2939.0|2973.1|3005.1|3039.0|3072.1|3104.1|3171.1|3172.1|3203.1|3205.1|3335.1|3336.1|3006.1|3434.1|3533.1|3566.0|988.1|3632.0|3732.0|3797.0|3863.0; request_uri=L29hdXRoL3Rva2Vu; referer_id=3; PHPSESSID=nnl4vk44bn4b5ti7haqqvg3864; ab_testing_theme=a; _ALGOLIA=anonymous-04c2bef0-986e-4197-8cda-2eb825d28d74; _hjSessionUser_919765=eyJpZCI6ImM5NDYzYjc1LTliOWUtNWRkYy1hOGE3LTFlNTcyOGRiMWMyOSIsImNyZWF0ZWQiOjE2ODg3MjgyMjY3MzAsImV4aXN0aW5nIjpmYWxzZX0=; _fbp=fb.1.1688728226860.823835840; _gid=GA1.2.1308908793.1688850622; _spmm_ses.1574=*; ln_or=eyIzOTIyNTUzIjoiZCJ9; _ga=GA1.2.1004305271.1687338429; _uetsid=d958d3c01dd311eea9fa29441a191757; _uetvid=0036c530101311ee91f7737f3b343b65; cto_bundle=mh6zzl81ZEJCZDBhWTZiUGxNQko5RzMzSWRoaWNrSlV3JTJCN1kwVUtuQzhxT2NyNGtkdk84N0g4VXc0dGF4OFowT254UTJWNWtibm9vMEY3dnVlZW9oOGZHNWppcXVwRHBtekh1dW9uSVV3QWlYOGt3WWRLcUtPSHFjT0s3bTM3cjRLOGslMkZ4VzVGaHFHdGxXMGdMb2JQRmdha0pWMElPZDdDWVdWYWQlMkJmYzAzaGhaTk40dyUyQmlEQUtzRm4lMkZLVjF4VSUyQkowM0o; ABTastySession=mrasn=&lp=https%253A%252F%252Fwww.manomano.fr%252Fmarque%252Fdewalt-3; _spmm_id.1574=28ae52a5-1de4-4639-bcb9-4d6b558099ce.1687338429.4.1688852220.1688737700.68b7e2ca-7e0e-418a-b2cb-aea1483ba39c; _ga_6WCFY7KGNT=GS1.1.1688850446.5.1.1688852220.59.0.0; amp_eb4016=lGzDD-a5vnOgQHK-QL3Y8E...1h4rl9eem.1h4rmvisp.6k.76.dq; OAuth_Token_Request_State=1ef1efc2-e9e4-456a-bc45-b850e34e3a1e; multireferer_id=a%3A1%3A%7Bi%3A3%3Bs%3A24%3A%222023-07-08T21%3A35%3A59%2B0000%22%3B%7D; __cf_bm=eNAyiWYG4OC9zYAV9cpOxXIt3UDDA4pT_O_iZxptCmE-1688852537-0-ASa7/RI+3FlJv1O3jSAQMB0spGsv6aeXgSGJkBGewmHe5MPONJdVpDvbT5Lhl0mD/lkFExyQGYreedwv9+mwjnC4sVtEit8xiCopWuVNa7/wavsj+y6pcsnCTRh+i/ucXw==; ABTasty=uid=wa81pcrygjp7g4gq&fst=1687338426869&pst=1688736589442&cst=1688850746501&ns=4&pvt=17&pvis=2&th='

    cookies_dict = {}
    for item in cookies_str.split('; '):
        key, value = item.split('=', maxsplit=1)
        cookies_dict[key] = value
    return cookies_dict


COOKIES = get_cookies_dict()


class WebscrapySpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

class WebscrapyDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request: Request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # request.cookies = COOKIES
        # request.meta = {'proxy': 'socks5://127.0.0.1:10808'}
        # ua = random.choice(USER_AGENT_LIST)
        # request.headers['User-Agent'] = ua
        # print(ua)
        # print(ua)

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

class RotateProxyMiddleware:
    def __init__(self, proxies_file):
        self.proxies_file = proxies_file
        self.proxies = self.load_proxies()
        self.current_proxy = None

    @classmethod
    def from_crawler(cls, crawler):
        proxies_file = crawler.settings.get('PROXIES_FILE')
        return cls(proxies_file)

    def load_proxies(self):
        with open(self.proxies_file, 'r') as file:
            proxies = file.read().splitlines()
        return proxies

    def process_request(self, request, spider):
        if not self.current_proxy:
            self.current_proxy = self.get_random_proxy()

        request.meta['proxy'] = self.current_proxy
        print('current_proxy')
        print(self.current_proxy)

    def process_response(self, request, response, spider):
        if response.status == 403:
            self.remove_current_proxy()
            self.current_proxy = self.get_random_proxy()
            new_request = request.copy()
            new_request.dont_filter = True  # Disable duplicate request filtering
            return new_request
        elif response.status == 307:
            self.remove_current_proxy()
            self.current_proxy = self.get_random_proxy()
            new_request = request.copy()
            new_request.dont_filter = True  # Disable duplicate request filtering
            return new_request
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, IgnoreRequest):
            # Handle IgnoreRequest exceptions
            if getattr(exception, 'response', None) is not None:
                return self.process_response(request, exception.response, spider)
            else:
                # IgnoreRequest without a response, re-raise the exception
                raise exception
        elif isinstance(exception, NotConfigured):
            # NotConfigured exception, re-raise it
            raise exception
        else:
            # Handle other exceptions
            self.remove_current_proxy()
            self.current_proxy = self.get_random_proxy()
            new_request = request.copy()
            new_request.dont_filter = True  # Disable duplicate request filtering
            return new_request

    def get_random_proxy(self):
        if not self.proxies:
            self.proxies = self.load_proxies()  # Reload proxies from the file if the list is empty
        return random.choice(self.proxies)

    def remove_current_proxy(self):
        if self.current_proxy in self.proxies:
            self.proxies.remove(self.current_proxy)