#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import time
import pymongo
from bs4 import BeautifulSoup


clint = pymongo.MongoClient()
db = clint['58project']
collection = db['url_list']
start_url = 'http://cs.58.com/shouji/'

def get_links_from(start_url,pages,who_sells=1):
    list_view = '{}{}/pn{}/'.format(start_url,str(who_sells),str(pages))
    print list_view
    html = requests.get(list_view)
    time.sleep(1)
    soup = BeautifulSoup(html.text,'lxml')
    if not soup.find('td','t'):
        return None
    for link in soup.select('td.t a.t'):
        item_link = link.get('href').split('?')[0]

        if 'cs' not in item_link :
            continue
        collection.insert({'url':item_link})
        print '插入url成功',item_link


def get_views(url):
    '''获取js加载的浏览量  需要在请求js链接的时候加上headers不然请求不到数据'''
    info_id = url.split('/')[-1].strip('x.shtml')
    api = 'http://jst1.58.com/counter?infoid={}'.format(info_id)

    headers = {

        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'Language:zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'bj58_id58s="RXp5VkR1M21tM0tVMzc5OQ=="; id58=c5/njVd1wDpW16ToCtyxAg==; als=0; city=bj; 58home=bj; ipcity=cc%7C%u957F%u6625%7C0; sessionid=7d7a05c7-566c-4ee8-9a33-f9491ffc295f; __utma=253535702.545205630.1467371246.1467371246.1467371246.1; __utmc=253535702; __utmz=253535702.1467371246.1.1.utmcsr=bj.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/pbdn/1/; myfeet_tooltip=end; 58tj_uuid=7dc55421-36df-4bfa-a534-0f7dd003862d; new_session=0; new_uv=3; utm_source=; spm=; init_refer=; final_history={}%2C26342559128371; bj58_new_session=0; bj58_init_refer=""; bj58_new_uv=3'.format(
            str(info_id)),
        'Host': 'jst1.58.com',
        'Referer': 'http://bj.58.com/pingbandiannao/{}x.shtml'.format(info_id),
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }
    js = requests.get(api,headers=headers)
    views = js.text.split('=')[-1]
    return views

def get_item_info(url): #解析商品详情页面的数据
    web_data = requests.get(url)
    time.sleep(1)
    soup = BeautifulSoup(web_data.text, 'lxml')
    data = {
        'title': soup.title.text,
        'price': soup.find_all('span',class_='c_f50')[0].text,
        'area': list(soup.select('.c_25d')[0].stripped_strings) if soup.find_all('span','c_25d') else None,
        'date': soup.select('.time')[0].text,
        'views': get_views(url)
    }
    print(data)



#get_links_from(start_url,1)
#get_item_info('http://cs.58.com/diannao/26962458251055x.shtml')
