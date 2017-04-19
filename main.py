#!/usr/bin/env python
# -*- coding:utf-8 -*-

from multiprocessing import Pool
from channel_extract import get_channel_urls
from page_parsing import get_links_from

start_url = 'http://cs.58.com/sale.shtml'
url_host = 'http://cs.58.com'


def get_all_links_from(start_url):
    for page_num in range(1,101):
        get_links_from(start_url,page_num)


if __name__ == '__main__':
    start_urls_list = get_channel_urls(start_url)
    pool = Pool()
    pool.map(get_all_links_from,start_urls_list)