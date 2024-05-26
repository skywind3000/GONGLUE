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
import os
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
        outname = f'html/ff6/c{c+1}.html'
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
# remove unnecessary elements
#----------------------------------------------------------------------
def purify_html(html) -> bs4.element.Tag:
    soup = bs4.BeautifulSoup(html, 'html.parser')
    top = soup.find('div', class_ = 'Mid2L_con')
    if not top:
        raise ValueError('cannot find Mid2L_con')
    p = top.find('div', class_ = 'post_ding_top').find('p')
    top.find('a', class_ = 'post_ding_top_down').decompose()
    top.find('div', class_ = 'Content_Paging').decompose()
    p = top.find('p', class_ = 'gs_nc_editor')
    while p:
        next = p.find_next_sibling()
        p.decompose()
        p = next
    from bs4 import Comment
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()
    for a in top.find_all('a'):
        href = a.get('href')
        if not href:
            continue
        if 'showimage' not in href:
            continue
        if not a.img:
            continue
        img = a.img
        a.unwrap()
        if img.get('data-src'):
            img.attrs['src'] = img.attrs['data-src']
            del img.attrs['data-src']
    for a in top.find_all('a'):
        a.unwrap()
    return top


#----------------------------------------------------------------------
# download images and change image url to local
#----------------------------------------------------------------------
def download_images(soup):
    crawler.ensure_dir('images/games/ff6')
    for img in soup.find_all('img'):
        src = img.get('src')
        if not src:
            continue
        if src.startswith('http://') or src.startswith('https://'):
            filename = crawler.image_local(src, 'images/games/ff6')
            img.attrs['src'] = f'../../{filename}'
            if not os.path.isfile(filename):
                print(f'downloading {filename}')
                crawler.download(src, filename)
            else:
                print(f'already downloaded {filename}')
    return 0


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
    def test3():
        html = crawler.read_file_content('html/ff6/c1.html')
        soup = purify_html(html)
        download_images(soup)
        print(soup)
        return 0
    test3()


