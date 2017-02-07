# -*- coding: utf-8 -*-
#
# FileName		: freehao123.py
# Description		:  freehao123 列表爬虫
# Version		: 0.1 beta 2
# Date			: 2017-01-17
#
from bs4 import BeautifulSoup
import requests
import time
class miniSpider:
    def __init__(self, starturl):
        self.starturl = starturl
        self.results = []
        self.urls = []

    def result(self):
        return self.results

    def parse_list(self,url,data=None):
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

    def parse_cycle(self,starturl):
        if starturl not in self.urls:
            self.urls.append(starturl) # 记录URL，防止重复爬取
            result = self.parse_list(starturl)
            if result != None:
                self.results.append(result.get('result'))
                for url in result.get('next'):
                    self.parse_cycle(url.get('href'))
        return None
    
    def catch(self):
        self.parse_cycle(self.starturl)

if __name__ == '__main__':
    freehao123 = miniSpider('https://www.freehao123.com/category/vps-zhuji/')
    freehao123.catch()
    print(freehao123.result())