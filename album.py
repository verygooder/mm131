# coding=utf-8
import requests
from bs4 import BeautifulSoup
import time
from random import randint
import re


class Album(object):
    """docstring for Album"""

    def __init__(self, url_entrance):
        super(Album, self).__init__()
        self.url_entrance = url_entrance
        self.get_basic_info()

    def get_advanced_info(self):
        self.page_count = self.count_page()
        self.pic_lst = self.generate_all_pics()
        self.cover = self.pic_lst[1]  # 第一图index为1

    def __repr__(self):
        return self.id + '(' + self.catalog + ')'

    def get_basic_info(self):
        url = self.url_entrance
        lst = url.split('/')
        self.id = lst[-1][: -5]
        self.catalog = lst[-2]

    def count_page(self):
        print('count %s' % self.__repr__)
        r = requests.get(self.url_entrance)
        soup = BeautifulSoup(r.content, 'html5lib')
        page_tag = soup.find('span', class_='page-ch')
        pages = int(page_tag.getText()[1:-1])
        time.sleep(randint(1, 4))
        return pages

    def generate_all_pics(self):
        start = 'http://img1.mm131.me/pic/' + self.id + '/'
        end = '.jpg'
        lst = [start + str(i) + end for i in range(0, self.page_count + 1)]
        return lst

    def make_album_html(self):
        filename = '../mm131pic/content/' + self.id + '.html'
        with open('./format.html', 'r') as f:
            html_format = f.read()
        result = ''
        for url in self.pic_lst:
            line1 = '<a target="_blank" href="%s">' % url
            line2 = '<img src="%s", height="320">' % url
            line3 = ' '
            line4 = '</a>'
            add = ''.join([line1, line2, line3, line4])
            result += add
        html = re.sub(r'\<insert\>', result, html_format)
        with open(filename, 'w') as f:
            f.write(html)

