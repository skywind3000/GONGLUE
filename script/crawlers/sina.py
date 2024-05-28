#! /usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# sina_index.py - 
#
# Created by skywind on 2024/05/28
# Last Modified: 2024/05/28 14:34:30
#
#======================================================================
import sys
import time
import os
import json
import bs4
import crawler

# pylint: disable=wrong-import-order
import gonglue    # noqa


#----------------------------------------------------------------------
# internal
#----------------------------------------------------------------------
HTML = os.path.join(crawler.CRAWLERS, 'html/sina/index')
JSON = os.path.join(crawler.CRAWLERS, 'html/sina/index.json')
URL1 = 'http://roll.games.sina.com.cn/cplm_handbooklist/yxgl/index.shtml'
URL2 = 'http://roll.games.sina.com.cn/cplm_handbooklist/yxmj1/index.shtml'
NUM1 = 449
NUM2 = 104

MARK1 = '《'
MARK2 = '》'


#----------------------------------------------------------------------
# download index
#----------------------------------------------------------------------
def download_index():
    crawler.ensure_dir(HTML)
    for n in range(1, NUM1 + 1):
        url = URL1[:-6] + f'_{n}.shtml'
        srcname = os.path.join(HTML, f'c{n}.html')
        crawler.download(url, srcname, True)
        print(f'{n}/{NUM1} {url}')
    for n in range(1, NUM2 + 1):
        url = URL2[:-6] + f'_{n}.shtml'
        srcname = os.path.join(HTML, f'm{n}.html')
        crawler.download(url, srcname, True)
        print(f'{n}/{NUM2} {url}')
    return 0


#----------------------------------------------------------------------
# parse index page
#----------------------------------------------------------------------
def parse_page(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    div = soup.find('div', class_ = 'listBlk')
    assert div
    ul = div.find('ul', class_ = 'hp_newslist')
    assert ul
    records = []
    for li in ul.find_all('li'):
        a = li.find('a')
        href = a.get('href')
        title = a.get_text().strip('\r\n\t ')
        em = li.find('em')
        date = em.get_text().strip('[]\r\n\t ')
        if MARK1 not in title or MARK2 not in title:
            continue
        p1 = title.find(MARK1)
        p2 = title.find(MARK2, p1)
        game = title[p1 + len(MARK1):p2].strip('\r\n\t ')
        item = (game, title, href, date)
        # print(item[:2])
        records.append(item)
    return records


#----------------------------------------------------------------------
# merge records
#----------------------------------------------------------------------
def index_merge(index, records):
    for game, title, href, date in records:
        if game not in index:
            index[game] = []
        index[game].append((title, href, date))
    return 0


#----------------------------------------------------------------------
# parse index
#----------------------------------------------------------------------
def parse_index():
    index = {}
    index['gonglue'] = {}
    index['miji'] = {}
    for n in range(1, NUM1 + 1):
        srcname = os.path.join(HTML, f'c{n}.html')
        html = crawler.read_file_content(srcname)
        lst = parse_page(html)
        print(f'{n}/{NUM1} c{n}.html')
        index_merge(index['gonglue'], lst)
    for n in range(1, NUM2 + 1):
        srcname = os.path.join(HTML, f'm{n}.html')
        html = crawler.read_file_content(srcname)
        lst = parse_page(html)
        print(f'{n}/{NUM2} m{n}.html')
        index_merge(index['miji'], lst)
    gonglue.write_json(JSON, index)
    return 0


#----------------------------------------------------------------------
# get index
#----------------------------------------------------------------------
def get_index():
    if not os.path.exists(JSON):
        download_index()
        parse_index()
    return gonglue.read_json(JSON)


#----------------------------------------------------------------------
# testing suit
#----------------------------------------------------------------------
if __name__ == '__main__':
    def test1():
        return 0
    def test2():
        download_index()
        parse_index()
        return 0
    def test3():
        index = gonglue.read_json(JSON)
        for game in index:
            size = len(index[game])
            print(game, size)
        return 0
    def test4():
        index = get_index()
        print(len(index))
        return 0
    test4()



