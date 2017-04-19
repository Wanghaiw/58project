#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup

start_url = 'http://cs.58.com/sale.shtml'
url_host = 'http://cs.58.com'
def get_channel_urls(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html,'lxml')
    links = soup.select('ul.ym-submnu > li > b > a')
    return [url_host+link.get('href') for link in links]




if __name__ == '__main__':
    urls_list = get_channel_urls(start_url)
