# coding=utf-8
import requests
from bs4 import BeautifulSoup
import time
from random import randint


class Album(object):
    """docstring for Album"""

    def __init__(self, url_entrance):
        super(Album, self).__init__()
        self.url_entrance = url_entrance
        self.get_basic_info()

    def get_advanced_info(self):
        self.page_count = self.count_page()
        self.pic_lst = self.generate_all_pics()
        self.cover = self.pic_lst[0]  # 小图index为0

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