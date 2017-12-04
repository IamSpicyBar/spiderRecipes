# -*- coding: utf-8 -*-

import re
import config
import utils


from scrapy.spider import CrawlSpider
from scrapy import Request
from scrapy.selector import Selector
from sqlhelper import SqlHelper
import datetime


class Recipe(CrawlSpider):
    name = "user_recipes"

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

    page = 1
    user_id = 0
    user_url = '/'

    def __init__(self, *a , **kw):
        super(Recipe, self).__init__(*a, **kw)

        self.dir_name = 'log/%s' % self.name
        self.sql = SqlHelper()
        self.init()
        utils.make_dir(self.dir_name)

    def init(self):
        command = (
            "CREATE TABLE IF NOT EXISTS {} ("
            "`id` INT(8) NOT NULL AUTO_INCREMENT,"
            "`name` CHAR(20) NOT NULL COMMENT 'recipe name',"
            "`url` TEXT NOT NULL COMMENT 'recipe url',"
            "`item_id` INT(8) NOT NULL COMMENT 'recipe ID',"
            "`user_id` INT(12) NOT NULL COMMENT 'user ID',"
            "`create_time` DATETIME NOT NULL,"
            "PRIMARY KEY(id),"
            "UNIQUE KEY `item_id` (`item_id`)"
            ") ENGINE=InnoDB".format(config.item_list_table)
        )

        self.sql.create_table(command)



    def start_requests(self):
        command = "SELECT * from {}".format(config.users_urls_table)
        data = self.sql.query(command)

        for i, user in enumerate(data):
            self.page = 1
            self.user_id = user[2]
            self.user_url = user[3]
            url = self.base_url + user[3] + 'created/?page=%d' % self.page
            utils.log(url)
            yield Request(
                url = url,
                headers = self.header,
                callback = self.parse_all,
                errback = self.error_parse,
            )




    def parse_all(self, response):
        utils.log(response.url)
        if response.status == 200:
            file_name = '%s/user.html' % (self.dir_name)
            self.save_page(file_name, response.body)
            recipes = response.xpath("//div[@class='recipes-280-full-width-list']/ul/li").extract()
            
            for recipe in recipes:
                sel = Selector(text = recipe)
                
                name = sel.xpath("//p[@class='name ellipsis red-font']/a/text()").extract_first().strip()
                url = sel.xpath("//p[@class='name ellipsis red-font']/a/@href").extract_first()
                item_id = url.split('/')[-2]
                u_id = self.user_id
                dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                msg = (None, name, url, item_id, u_id, dt)
                command = ("INSERT IGNORE INTO {} "
                            "(id, name, url, item_id, user_id, create_time)"
                            "VALUES(%s,%s,%s,%s,%s,%s)".format(config.item_list_table)
                )
                self.sql.insert_data(command, msg)

            self.page += 1
            
            yield Request(
                url = self.base_url + self.user_url + 'created/?page=%d' % self.page,
                headers = self.header,
                callback = self.parse_all,
                errback = self.error_parse,
                dont_filter = true,
            )   

    def error_parse(self, faiture):
        request = faiture.request
        utils.log('error_parse url:%s meta:%s' % (request.url, request.meta))


    def save_page(self, file_name, data):
        with open(file_name, 'w') as f:
            f.write(data)
            f.close()

