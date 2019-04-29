#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   spidertest_maoyan.py
@Time    :   2019/04/26 09:12:32
@Author  :   BBCPicker
@Version :   1.0
@Contact :   291294719@qq.com
@Desc    :   爬虫测试--猫眼电影排行
'''

import requests
from requests.exceptions import RequestException
import re
import json
import time

'''
获取页面源代码
'''
def get_one_page(url):
    try:
        headers = {
            'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'
        }
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

'''
解析需要的信息
'''
def parse_one_page(html):
    pattern = re.compile(
        r'<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
            + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
            + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)

    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }

'''
将解析好的信息写入文件
'''
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+ '\n')

def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)
        time.sleep(1)