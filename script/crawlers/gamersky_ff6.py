#! /usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# gamersky_ff6.py - 
#
# Created by skywind on 2024/05/26
# Last Modified: 2024/05/26 04:52:25
#
#======================================================================
import sys
import time
import pprint
import bs4

import crawler


#----------------------------------------------------------------------
# global
#----------------------------------------------------------------------
URL = 'https://www.gamersky.com/handbook/201512/694858.shtml'


#----------------------------------------------------------------------
# 
#----------------------------------------------------------------------
def download_html():
    crawler.ensure_dir('html/ff6')
    for c in range(31):
        if c == 0:
            url = URL
        else:
            url = URL[:-6] + f'_{c+1}.shtml'
        print(f'downloading {url}')
        outname = f'html/ff6/c{c}.html'
        crawler.download(url, outname)
    return 0


#----------------------------------------------------------------------
# 
#----------------------------------------------------------------------
def analyze_toc(html):
    toc = []
    soup = bs4.BeautifulSoup(html, 'html.parser')
    div = soup.find('div', class_ = 'Content_Paging')
    assert div
    for li in div.find_all('li'):
        a = li.find('a')
        if not a:
            continue
        href = a.get('href')
        title = a.get_text()
        toc.append((title, href))
    return toc


#----------------------------------------------------------------------
# testing suit
#----------------------------------------------------------------------
if __name__ == '__main__':
    def test1():
        html = crawler.read_file_content('html/gamersky_ff6.html')
        toc = analyze_toc(html)
        pprint.pprint(toc)
        return 0
    def test2():
        download_html()
        return 0
    test1()


