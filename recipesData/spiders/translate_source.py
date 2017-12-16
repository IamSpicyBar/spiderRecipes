# -*- coding: utf-8 -*-

import re
import config
import utils


from scrapy.spider import CrawlSpider
from scrapy import Request
from scrapy.selector import Selector
from sqlhelper import SqlHelper


class translateSource(CrawlSpider):

    name = "translate_source"

    base_url = "http"
