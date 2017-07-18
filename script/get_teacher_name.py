import re
import os
import requests
from pypinyin import lazy_pinyin
from bs4 import BeautifulSoup as Bs
from . import HEADERS, PATH, store_data

BASE_URL = 'http://www.ucas.ac.cn/site/'
URL_NUM_LIST = [74, 232, 75, 76, 77, 78]
NAME_LIST = set()
FILE_NAME = os.path.join(PATH, 'src', 'AllNameList.txt')

print(FILE_NAME)


def get_page(num):
    url = BASE_URL + str(num)
    print(url)
    response = requests.get(url=url, headers=HEADERS)
    html = Bs(response.text, 'html.parser')
    return html


def get_name_list(html):
    for teacher_div in html.find_all('div', class_="yp_ity"):
        for teacher in teacher_div.find_all('a', target="_blank"):
            name = teacher.get('title')
            if not is_have_english(name):
                name_pinyin = name_to_pinyin(name)
                # if name_pinyin not in NAME_LIST:
                #     NAME_LIST.append(name_pinyin)
                NAME_LIST.add(name_pinyin)


def name_to_pinyin(name):
    '汉字转拼音'
    pinyin_list = lazy_pinyin(name, errors='ignore')
    pinyin = ''.join(pinyin_list)
    return pinyin


def is_have_english(name):
    '有英文返回True, 没有返回False'
    en_pattern = re.compile('[a-zA-Z]+')
    return en_pattern.search(name)


def main():
    '主函数'
    for num in URL_NUM_LIST:
        html = get_page(num)
        get_name_list(html)
    store_data(FILE_NAME, NAME_LIST)


if __name__ == '__main__':
    main()
