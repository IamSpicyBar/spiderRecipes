#-*- coding: utf-8 -*-


#First get users urls
#Then get recipes for each user
import logging
import os
import sys
import utils

from scrapy import cmdline

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    if not os.path.exists('log'):
        os.makedirs('log')

    logging.basicConfig(
        filename = 'log/item.log',
        format = '%(levelname)s %(asctime)s: %(message)s',
        level = logging.DEBUG
    )

    while True:
        utils.log('*******************run spider start...*******************')
        #cmdline.execute('scrapy crawl user_urls'.split())
        #cmdline.execute('scrapy crawl user_recipes'.split())
        cmdline.execute('scrapy crawl recipe_detail'.split())
