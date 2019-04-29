#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   spidertest_zhihu.py
@Time    :   2019/04/26 15:23:57
@Author  :   BBCPicker
@Version :   1.0
@Contact :   291294719@qq.com
@Desc    :   爬取知乎热门话题，练习python存储
'''

import requests
from pyquery import PyQuery as pq

url = 'https://www.zhihu.com/explore'
headers = {
            'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'
        }

html = requests.get(url,headers=headers).text
doc = pq(html)

items = doc('.explore-tab .feed-item').items()
for item in items:
    question = item.find('h2').text()
    author = item.find('.author-link-line').text()
    answer = pq(item.find('.content').html()).text() # 如果内容含有html格式需要先用pyquery把html格式去掉
    file = open('explore.txt', 'a', encoding='utf-8')
    file.write('\n'.join([question,'--------------', author,'--------------', answer]))
    file.write('\n' + '=' * 50 + '\n')
    file.write('\n' * 3)
    file.close()
