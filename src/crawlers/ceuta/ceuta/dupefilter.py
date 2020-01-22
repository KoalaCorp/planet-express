import logging
import time

from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint

from . import defaults
from .connection import get_redis_from_settings


logger = logging.getLogger(__name__)


# TODO: Rename class to RedisDupeFilter.
class RedisDupeFilter(BaseDupeFilter):
    """Redis-based request duplicates filter.

    This class can also be used with default Scrapy's scheduler.

    """

    logger = logger

    def __init__(self, server, expire_secs, debug=False):
        """Initialize the duplicates filter.

        Parameters
        ----------
        server : redis.StrictRedis
            The redis server instance.
        expire_secs : int
            seconds when a key is expired
        debug : bool, optional
            Whether to log filtered requests.

        """
        self.server = server
        self.expire_secs = expire_secs
        self.debug = debug
        self.logdupes = True

    @classmethod
    def from_settings(cls, settings):
        """Returns an instance from given settings.
        This uses by default the key ``dupefilter:<timestamp>``. When using the
        ``scrapy_redis.scheduler.Scheduler`` class, this method is not used as
        it needs to pass the spider name in the key.
        Parameters
        ----------
        settings : scrapy.settings.Settings
        Returns
        -------
        RFPDupeFilter
            A RFPDupeFilter instance.
        """
        server = get_redis_from_settings(settings)
        # XXX: This creates one-time key. needed to support to use this
        # class as standalone dupefilter with scrapy's default scheduler
        # if scrapy passes spider on open() method this wouldn't be needed
        # TODO: Use SCRAPY_JOB env as default and fallback to timestamp.
        debug = settings.getbool('DUPEFILTER_DEBUG')
        expire_secs = settings.get("EXPIRE_REDIS_KEY",
                                   defaults.EXPIRE_REDIS_KEY)
        print("*"*100)
        print("FROM SETTINGS")
        return cls(server, expire_secs=expire_secs, debug=debug)
    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #     """Returns instance from crawler.
    #     Parameters
    #     ----------
    #     crawler : scrapy.crawler.Crawler
    #     Returns
    #     -------
    #     RFPDupeFilter
    #     Instance of RFPDupeFilter.
    #     """
    #     print("*"*100)
    #     print("FROM CRAWLER")
    #     return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        """Returns True if request was already seen.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        bool

        """
        # import ipdb; ipdb.set_trace()
        key = self.request_fingerprint(request)
        last_timestamp = self.server.get(key)
        now_timestamp = time.time()
        if not last_timestamp or\
           (now_timestamp - float(last_timestamp)) > self.expire_secs:
            self.server.set(key, now_timestamp)
        else:
            return True

    def request_fingerprint(self, request):
        """Returns a fingerprint for a given request.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        str

        """
        return request_fingerprint(request)
    #
    # @classmethod
    # def from_spider(cls, spider):
    #     settings = spider.settings
    #     server = get_redis_from_settings(settings)
    #     expire_secs = settings.get("EXPIRE_REDIS_KEY",
    #                                defaults.EXPIRE_REDIS_KEY)
    #     debug = settings.getbool('DUPEFILTER_DEBUG')
    #     print("*"*100)
    #     print("FROM SPIDER")
    #     return cls(server, expire_secs=expire_secs, debug=debug)

    def close(self, reason=''):
        """Delete data on close. Called by Scrapy's scheduler.

        Parameters
        ----------
        reason : str, optional

        """
        pass

    def log(self, request, spider):
        """Logs given request.

        Parameters
        ----------
        request : scrapy.http.Request
        spider : scrapy.spiders.Spider

        """
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg,
                              {'request': request},
                              extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg,
                              {'request': request},
                              extra={'spider': spider})
            self.logdupes = False
