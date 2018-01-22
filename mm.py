# coding=utf-8
import requests
import re
import os
from album import Album
import time


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
        os.mkdir('../mm131pic/content')
        os.system('touch ../mm131pic/exist')
    else:
        if os.path.exists('../mm131pic/exist') is False:
            os.system('touch ../mm131pic/exist')
        if os.path.exists('../mm131pic/content') is False:
            os.mkdir('../mm131pic/content')


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


def make_main_html(pic_obj_lst):
    current_time = time.localtime()
    year = current_time.tm_year
    month = current_time.tm_mon
    date = current_time.tm_mday
    tail = str(len(pic_obj_lst)) + 'items'
    time_join = '%s+%s+%s+%s' % (year, month, date, tail)
    filename = '../mm131pic/%s.html' % time_join
    with open('./format.html', 'r') as f:
        html_format = f.read()
    result = ''
    for pic in pic_obj_lst:
        cover_url = pic.cover
        direct_target = './content/' + pic.id + '.html'
        line1 = '<a target="_blank" href="%s">' % direct_target
        line2 = '<img src="%s", height="320">' % cover_url
        line3 = ' '
        line4 = '</a>'
        add = ''.join([line1, line2, line3, line4])
        result += add
    html = re.sub(r'\<insert\>', result, html_format)
    with open(filename, 'w') as f:
        f.write(html)


if __name__ == "__main__":
    header = get_main_header()
    all_pic_lst = get_main_info(header)
    all_pic_lst = list(set(all_pic_lst))
    retain_pic_lst = de_reduntant(all_pic_lst)
    if retain_pic_lst:
        pics = [Album(i) for i in retain_pic_lst]
        for i in pics:
            i.get_advanced_info()
        for i in pics:
            i.make_album_html()
        # pics = make_parts_html(pics)
        make_main_html(pics)
