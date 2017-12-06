# -*- coding: utf-8 -*-

import re
import config
import utils


from scrapy.spider import Spider
from scrapy import Request
from scrapy.selector import Selector
from sqlhelper import SqlHelper
import datetime


class User(Spider):
    name = "user_urls"

    start_url = 'https://www.xiachufang.com'

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
        super(User, self).__init__(*a, **kw)

        self.dir_name = 'log/%s' % self.name
        self.sql = SqlHelper()
        self.init()
        utils.make_dir(self.dir_name)


    def init(self):
        command = (
            "CREATE TABLE IF NOT EXISTS {} ("
            "`id` INT(8) NOT NULL AUTO_INCREMENT,"
            "`name` CHAR(20) NOT NULL COMMENT 'user_name',"
            "`user_id` INT(12) NOT NULL COMMENT 'user_ID',"
            "`url` TEXT NOT NULL COMMENT 'user_url',"
            "`create_time` DATETIME NOT NULL,"
            "PRIMARY KEY(id),"
            "UNIQUE KEY `user_id` (`user_id`)"
            ") ENGINE=InnoDB".format(config.users_urls_table)
        )

        self.sql.create_table(command)

    def start_requests(self):
        active_url = '/feature/cook/active/'
        url = self.start_url + active_url
        N = 5
        
        for index in range(1,N):
            yield Request(
                url = url,
                headers = self.header,
                callback = self.parse_all,
                errback = self.error_parse,
                dont_filter = True,
            )


    def parse_all(self, response):
        if response.status == 200:
            file_name = '%s/users.html' % (self.dir_name)
            self.save_page(file_name, response.body)
            users = response.xpath("//div[@class='content']/ul/li").extract()
            for user in users:
                sel = Selector(text = user)

                url = sel.xpath("//div[@class='name']/a/@href").extract_first()
                user_id = url.split('/')[-2]
                name = sel.xpath("//div[@class='name']/a/text()").extract_first()
                dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                msg = (None , name, user_id, url, dt)
                command = ("INSERT IGNORE INTO {} "
                            "(id, name, user_id, url, create_time)"
                            "VALUES(%s,%s,%s,%s,%s)".format(config.users_urls_table)
                )
                self.sql.insert_data(command, msg)

                




    def error_parse(self, faiture):
        request = faiture.request
        utils.log('error_parse url:%s meta:%s' % (request.url, request.meta))


    def save_page(self, file_name, data):
        with open(file_name, 'w') as f:
            f.write(data)
            f.close()
