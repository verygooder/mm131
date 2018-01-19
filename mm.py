# coding=utf-8
import requests
import re
import os
from album import Album


def get_main_header():
    # 生成requests需要的headers
    with open('./main_header.txt', 'r') as f:
        data = f.readlines()
    data = [i.strip() for i in data]
    header_dic = {}
    for line in data:
        index = line.find(':')
        key = line[: index]
        value = line[index + 2:]
        header_dic[key] = value
    return header_dic


def get_main_info(header):
    # 取得主页所有图片的url list
    url = 'http://www.mm131.com/'
    r = requests.get(url, headers=header)
    if r.status_code == 200:
        html = r.text
    else:
        print('cant load main page.')
        html = ''
        # exit()
    reg = r'http://www.mm131.*?html'
    lst = re.findall(reg, html)
    return lst


def detect_exist():
    # 如果../mm131pic/exist不存在，就创建一个
    if os.path.exists('../mm131pic/') is False:
        os.mkdir('../mm131pic')
        os.system('touch ../mm131pic/exist')
    else:
        if os.path.exists('../mm131pic/exist') is False:
            os.system('touch ../mm131pic/exist')


def de_reduntant(lst_in):
    # 与exist比较，去除重复项，返回非重复项，并写入exist
    lst = lst_in[:]
    detect_exist()
    with open('../mm131pic/exist', 'r') as f:
        data = f.readlines()
    data = [i.strip() for i in data]
    lst = [i for i in lst if i not in data]
    with open('../mm131pic/exist', 'a') as f:
        for line in lst:
            f.writelines(line + '\n')
    print('write %s items in exist' % str(len(lst)))
    return lst


header = get_main_header()
all_pic_lst = get_main_info(header)
retain_pic_lst = de_reduntant(all_pic_lst)
pics = [Album(i) for i in retain_pic_lst]
