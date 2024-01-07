import time
import asyncio
import json

from scrapy import signals

class TokenBucket(object):
    def __init__(self, name: str, capacity: float, fill_rate: float):
        """
        params:
        name (str): name of token bucket
        capacity (float): token bucket capacity
        fill_rate (float): token fill rate
        """
        self.name = name
        self.capacity = float(capacity)
        self.tokens = float(capacity)
        self.fill_rate = float(fill_rate)
        self.timestamp = time.time()

    def __str__(self):
        return json.dumps(self.__dict__)

    def consume(self, tokens: float) -> bool:
        """
        consume token

        params:
        tokens (float): tokens to be consume

        return:
        bool: consume ok or failed
        """
        if self.tokens < self.capacity:
            now = time.time()
            delta = self.fill_rate * (now - self.timestamp)
            self.tokens = min(self.capacity, self.tokens + delta)
            self.timestamp = now

        if tokens <= self.tokens:
            self.tokens -= tokens
            return True
        else:
            return False

    def delay(self, tokens: float) -> float:
        """
        calculate delay seconds to wait tokens ready

        params:
        tokens (float): tokens to be consume

        return:
        float: need delay seconds
        """
        if self.tokens > tokens:
            return 0
        return (tokens - self.tokens) / self.fill_rate

class QosDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self, settings: dict):
        self.settings = settings
        self.iops_limit = None
        if settings.get('QOS_IOPS_ENABLED', False):
            capacity = settings.get('QOS_IOPS_CAPACITY', 1)
            iops_limit = settings.get('QOS_IOPS_LIMIT', 1)
            self.iops_limit = TokenBucket('iops', capacity, iops_limit)

        self.bps_limit = None
        if settings.get('QOS_BPS_ENABLED', False):
            capacity = settings.get('QOS_BPS_CAPACITY', 1<<20)
            bps_limit = settings.get('QOS_BPS_LIMIT', 1<<20)
            self.bps_limit = TokenBucket('bps', capacity, bps_limit)

        self.small_response_size = settings.get('QOS_SMALL_RESPONSE_SIZE', 0)
        self.guess_response_len = 1<<20

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(crawler.settings)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    async def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        if self.iops_limit:
            while not self.iops_limit.consume(1):
                await asyncio.sleep(self.iops_limit.delay(1))

        if self.bps_limit:
            while not self.bps_limit.consume(self.guess_response_len):
                await asyncio.sleep(self.bps_limit.delay(self.guess_response_len))

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        if len(response.body) >= self.small_response_size:
            a = 0.8
            self.guess_response_len = (1 - a) * self.guess_response_len + a * len(response.body)

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
        self.spider = spider
        spider.logger.info(f"Spider opened: {spider.name} with QosDownloaderMiddleware iops:{self.iops_limit}, bps:{self.bps_limit}")