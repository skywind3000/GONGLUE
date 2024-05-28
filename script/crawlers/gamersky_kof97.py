#! /usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# gamersky_kof97.py - 
#
# Created by skywind on 2024/05/28
# Last Modified: 2024/05/28 07:11:12
#
#======================================================================
import sys
import os
import time
import pprint
import bs4
import crawler
import gamersky

sys.path.append(crawler.SCRIPT)
# pylint: disable=wrong-import-order,wrong-import-position
import gonglue  # noqa


#----------------------------------------------------------------------
# INTERNAL
#----------------------------------------------------------------------
HTML = os.path.join(crawler.CRAWLER, 'html/games/kof97')
URL = 'https://www.gamersky.com/handbook/201804/1032863.shtml'
NUM = 34


#----------------------------------------------------------------------
# down chapters
#----------------------------------------------------------------------
def download_pages():
    if not os.path.isdir(HTML):
        os.makedirs(HTML)
    for n in range(1, NUM + 1):
        if n == 1:
            url = URL
        else:
            url = URL[:-6] + f'_{n}.shtml'
        srcname = os.path.join(HTML, f'c{n}.html')
        srcname = os.path.normpath(srcname)
        srcname = os.path.relpath(srcname)
        if crawler.download(url, srcname, True):
            # print(f'skip {srcname}')
            pass
    return 0


#----------------------------------------------------------------------
# 
#----------------------------------------------------------------------
def parse_pages():
    content = []
    for n in range(1, NUM + 1):
        srcname = os.path.join(HTML, f'c{n}.html')
        html = gonglue.read_file_content(srcname)
        md = parse_html(html)
        content.append(md + '\n')
        # break
    open('html/games/kof97.md', 'w', encoding = 'utf-8').write(''.join(content))
    return 0


#----------------------------------------------------------------------
# 
#----------------------------------------------------------------------
def parse_html(html):
    root = gamersky.purify_html(html)
    crawler.localize_image(root, 'images/games/gamersky', '../../images/games/gamersky/')
    opts = {}
    md = crawler.html_to_markdown(root, **opts)
    md = crawler.merge_empty_lines(md)
    md = md.strip('\r\n\t ')
    if md.endswith('更多相关内容请关注：拳皇97专区'):
        md = md[:-len('更多相关内容请关注：拳皇97专区')].strip('\r\n\t ')
    md = f'## {md}\n'
    print(md)
    return md


#----------------------------------------------------------------------
# testing suit
#----------------------------------------------------------------------
if __name__ == '__main__':
    def test1():
        download_pages()
        parse_pages()
        return 0
    test1()

