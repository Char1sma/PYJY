# -*- coding: utf-8 -*-
#
# FileName		: freehao123.py
# Description		:  freehao123 列表爬虫
# Version		: 0.1 beta
# Date			: 2017-01-16
#
from bs4 import BeautifulSoup
import requests
import time
def parse_list(url,data=None):
    info = []
    wb_data = requests.get(url)
    Soup = BeautifulSoup(wb_data.text,'lxml')
    pTitle = Soup.select('body > div#page > div#center > div.col > [id^="post"] > h4 > a')
    pContent = Soup.select('body > div#page > div#center > div.col > [id^="post"] > .postcontent')
    pMeta = Soup.select('body > div#page > div#center > div.col > [id^="post"] > .postmeat')
    pPages = Soup.select('div.wp-pagenavi > a') # 翻页导航
    for title,content,meta in zip(pTitle,pContent,pMeta):
        data = {
            'title':title.get_text(),
            'content':content.get_text(),
            'meta':meta.get_text()
        }
        info.append(data)
    result = {
        'next': pPages,
        'result': info
    }
    time.sleep(1)
    return result

def parse_freehao(starturl,urls ,results):
    if starturl not in urls:
        urls.append(starturl) # 记录URL，防止重复爬取
        result = parse_list(starturl)
        if result != None:
            results.append(result.get('result'))
            for url in result.get('next'):
                parse_freehao(url.get('href'),urls,results)
    return None

urls = []
results = []
parse_freehao('https://www.freehao123.com/category/vps-zhuji/',urls,results)
print(results)