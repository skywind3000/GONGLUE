#! /usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# gamersky.py - 
#
# Created by skywind on 2024/05/28
# Last Modified: 2024/05/28 07:27:01
#
#======================================================================
import sys
import os
import time
import bs4
import crawler


sys.path.append(crawler.SCRIPT)
# pylint: disable=wrong-import-order,wrong-import-position
import gonglue  # noqa


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
# testing suit
#----------------------------------------------------------------------
if __name__ == '__main__':
    def test1():
        
        return 0
    test1()




