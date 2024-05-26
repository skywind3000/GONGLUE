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
                # print(f'already downloaded {filename}')
                pass
    return 0


#----------------------------------------------------------------------
# 
#----------------------------------------------------------------------
def table_unwrap(soup: bs4.element.Tag):
    for table in soup.find_all('table', class_ = 'table2'):
        td1 = table.td
        td2 = td1.find_next_sibling()
        if td2.img:
            td1, td2 = td2, td1
        div = bs4.BeautifulSoup('<div></div>', 'html.parser').div
        p1 = bs4.BeautifulSoup('<p></p>', 'html.parser').p
        p2 = bs4.BeautifulSoup('<p></p>', 'html.parser').p
        p1.append(td1)
        p2.append(td2)
        div.append(p1)
        div.append(p2)
        table.replace_with(div)
        td1.unwrap()
        td2.unwrap()
    return 0


#----------------------------------------------------------------------
# 
#----------------------------------------------------------------------
def clear_markdown(md: str):
    md = md.strip('\r\n')
    md = crawler.merge_empty_lines(md)
    foot = '更多相关内容请关注：最终幻想6专区'
    if md.endswith(foot):
        md = md[:-len(foot)].strip('\r\n\t ')
        md += '\n'
    md = '\n'.join(md.split('\n')[1:]).lstrip('\r\n')
    content = []
    for line in md.split('\n'):
        line = line.rstrip('\r\n\t ')
        if line.startswith('**') and line.endswith('**'):
            line = line[2:-2]
            line = '## ' + line
        content.append(line)
    return '\n'.join(content)


#----------------------------------------------------------------------
# 
#----------------------------------------------------------------------
def export_markdown():
    merge = []
    merge.append('# 最终幻想6攻略')
    merge.append('')
    for chapter in range(1, 32):
        srcname = f'html/ff6/c{chapter}.html'
        dstname = f'html/ff6/m{chapter}.md'
        print('processing', srcname)
        html = crawler.read_file_content(srcname)
        soup = purify_html(html)
        download_images(soup)
        table_unwrap(soup)
        opts = {}
        md = crawler.html_to_markdown(soup, **opts)
        md = clear_markdown(md)
        open(dstname, 'w', encoding = 'utf-8').write(md)
        merge.append(md)
        merge.append('')
    md = '\n'.join(merge)
    open('html/ff6/ff6.md', 'w', encoding = 'utf-8').write(md)
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
        table_unwrap(soup)
        print(soup)
        return 0
    def test4():
        html = crawler.read_file_content('html/ff6/c1.html')
        soup = purify_html(html)
        download_images(soup)
        table_unwrap(soup)
        opts = {}
        # opts['strip'] = ['table']
        # opts['convert'] = ['img']
        opts['keep_inline_images_in'] = ['td', 'div', 'tr']
        md = crawler.html_to_markdown(soup, **opts)
        print(md)
        return 0
    def test5():
        export_markdown()
        return 0
    test5()


