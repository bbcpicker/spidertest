#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   spidertest_weibo.py
@Time    :   2019/04/26 16:29:47
@Author  :   BBCPicker
@Version :   1.0
@Contact :   291294719@qq.com
@Desc    :   以微博网页练习python的Ajax数据爬取
'''

from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq

base_url = 'https://m.weibo.cn/api/container/getIndex?'

headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/p/second?',
    'User-Agent': 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'X-Request-With': 'XMLHttpRequest'
}

def get_page(page):
    params = {
        'type': 'uid',
        'value': '2390672577',# 用户id 唯一
        'containerid': '1076032390672577', # 107603+用户id
        'page': page
    }
    url = base_url + urlencode(params)
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)

def parse_page(json):
    if json:
        items = json.get('data').get('cards')
        for item in items:
            try:
                item = item.get('mblog')
                weibo = {}
                weibo['id'] = item.get('id')
                weibo['text'] = pq(item.get('text')).text()
                weibo['attitudes'] = item.get('attitudes_count')
                weibo['comments'] = item.get('comments_count')
                weibo['reposts'] = item.get('reposts_count')
                yield weibo
            except Exception:
                continue

if __name__ == '__main__':
    for page in range(1,11):
        json = get_page(page)
        # print(json)
        results = parse_page(json)
        for result in results:
            file = open('weibo.txt', 'a', encoding='utf-8')
            id = result['id']
            text = result['text']
            attitudes = result['attitudes']
            comments = result['comments'] 
            reposts = result['reposts']
            file.write('\n' + '微博id' + id + '-----内容：' + text + '-----点赞数：' + str(attitudes) +'-----评论数：' + str(comments) + '-----转发数：' + str(reposts))
            file.write('\n' + '=' * 50 + '\n')
            file.write('\n' * 3)
            file.close()
