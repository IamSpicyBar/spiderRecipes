# -*- coding: utf-8 -*-

import re
import config
import utils


from scrapy.spider import CrawlSpider
from scrapy import Request
from scrapy.selector import Selector
from sqlhelper import SqlHelper
import datetime


class RecipeDetail(CrawlSpider):
    name = "recipe_detail"

    base_url = 'https://www.xiachufang.com'
    
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection': 'keep-alive',
        'Host': 'www.xiachufang.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:51.0) Gecko/20100101 Firefox/51.0',
    }

    

    def __init__(self, *a , **kw):
        super(RecipeDetail, self).__init__(*a, **kw)

        self.dir_name = 'log/%s' % self.name
        self.sql = SqlHelper()
        self.init()
        utils.make_dir(self.dir_name)


    def init(self):
        command = (
            "CREATE TABLE IF NOT EXISTS {} ("
            "`id` INT(8) NOT NULL AUTO_INCREMENT,"
            "`name` CHAR(20) NOT NULL COMMENT 'recipe name',"
            "`recipe_id` INT(12) NOT NULL COMMENT 'recipe ID',"
            "`source_name` CHAR(20) NOT NULL COMMENT 'source name',"
            "`source_id` INT(8) NOT NULL COMMENT 'source ID',"
            "`create_time` DATETIME NOT NULL,"
            "PRIMARY KEY(id)"
            ") ENGINE=InnoDB".format(config.item_detail_table)
        )

        self.sql.create_table(command)

    def start_requests(self):
        command = "SELECT * from {}".format(config.item_list_table)
        data = self.sql.query(command)

        for i, recipe in enumerate(data):
            if recipe[0] > 8999 and recipe[0] < 10000:
                url = self.base_url + recipe[2]
                utils.log(url)
                yield Request(
                    url = url,
                    headers = self.header,
                    callback = self.parse_all,
                    errback = self.error_parse,
                    meta={"re_id": recipe[3], "re_name": recipe[1]},
                    dont_filter = True,
                )


    def parse_all(self, response):
        utils.log(response.url)
        if response.status == 429:
            raise CloseSpider('Too much request, IP banned')
        if response.status == 200:
            file_name = '%s/recipe.html' % (self.dir_name)
            self.save_page(file_name, response.body)
            sources = response.xpath("//div[@class='ings']//tr").extract()

            for source in sources:
                sel = Selector(text = source)
                
                source_name = sel.xpath("//a/text()").extract_first()
                url = sel.xpath("//a/@href").extract_first()
                if source_name is not None and url is not None:
                    source_id = url.split('/')[-2]
                    r_name = response.meta["re_name"]
                    r_id = response.meta["re_id"]
                    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    msg = (None, r_name, r_id, source_name, source_id, dt)
                    command = ("INSERT IGNORE INTO {} "
                                "(id, name, recipe_id, source_name, source_id, create_time)"
                                "VALUES(%s,%s,%s,%s,%s,%s)".format(config.item_detail_table)
                    )
                    self.sql.insert_data(command, msg)


    def error_parse(self, faiture):
        request = faiture.request
        utils.log('error_parse url:%s meta:%s' % (request.url, request.meta))


    def save_page(self, file_name, data):
        with open(file_name, 'w') as f:
            f.write(data)
            f.close()

