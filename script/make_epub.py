#! /usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# make_epub.py - 
#
# Created by skywind on 2024/05/24
# Last Modified: 2024/05/24 01:38:26
#
#======================================================================
import sys
import time
import os
import bs4
from ebooklib import epub
import gonglue


#----------------------------------------------------------------------
# change image/css url: because epub requires all xhtml files in 
# the root directory, so we need to change the image/css url
#----------------------------------------------------------------------
def patch_html(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all('img'):
        src = tag.get('src')
        if src:
            pos = src.find('/images/')
            if pos >= 0 and src.startswith('../'):
                tag['src'] = 'images/' + src[pos + 8:]
    for tag in soup.find_all('link'):
        href = tag.get('href')
        if href:
            pos = href.find('/images/')
            if pos >= 0:
                tag['href'] = 'images/' + href[pos + 8:]
    for tag in soup.find_all('a'):
        href = tag.get('href')
        if href:
            if href.startswith('http://') or href.startswith('https://'):
                tag['target'] = '_blank'
    html = str(soup)
    return html


#----------------------------------------------------------------------
# Epub Book
#----------------------------------------------------------------------
class EpubBook (object):

    def __init__ (self):
        self.htmls = gonglue.list_html()

    def init (self):
        self.book = epub.EpubBook()
        book = self.book
        uuid = 'GAMEGUIDE-LW-' + time.strftime('%Y%m%d%H%M%S')
        book.set_identifier(uuid)
        book.set_title('游戏攻略合集')
        book.set_language('zh-CN')
        book.add_author('skywind')
        book.toc = []
        book.spine = []
        self.css_epub = None
        self.css_nav = None
        image = os.path.join(gonglue.PROJECT, 'images/cover.jpg')
        book.set_cover('cover.jpg', open(image, 'rb').read())
        cover: epub.EpubItem = book.get_item_with_id('cover')
        cover.is_linear = True
        book.spine = ['cover', 'nav']

    def add_html (self, debug = False):
        book = self.book
        mode = 1
        index = 0
        category = 0
        if '*' in self.htmls:
            for fn in self.htmls['*']:
                title = self.htmls['*'][fn]
                srcname = f'html/{fn}'
                dstname = f'html/{index}.xhtml'
                dstname = f'c{index}.xhtml'
                index += 1
                print(srcname)
                filename = os.path.join(gonglue.BUILD, srcname)
                item = epub.EpubHtml(title=title, file_name=dstname)
                item.content = gonglue.read_file_content(filename)
                item.content = patch_html(item.content)
                item.media_type = 'application/xhtml+xml'
                item.add_item(self.css_epub)
                book.add_item(item)
                book.spine.append(item)
                book.toc.append(item)
        for dirname in self.htmls:
            count = 0
            if dirname == '*':
                continue
            entry = f'{category}'
            category += 1
            section = [epub.Section(dirname), []]
            for fn in self.htmls[dirname]:
                title = self.htmls[dirname][fn]
                srcname = f'html/{dirname}/{fn}'
                dstname = f'html/{entry}/{index}.xhtml'
                dstname = f'c{index}.xhtml'
                index += 1
                print(srcname)
                filename = os.path.join(gonglue.BUILD, srcname)
                item = epub.EpubHtml(title=title, file_name=dstname)
                item.content = gonglue.read_file_content(filename)
                item.content = patch_html(item.content)
                item.media_type = 'application/xhtml+xml'
                item.add_item(self.css_epub)
                book.add_item(item)
                book.spine.append(item)
                section[1].append(item)
                count += 1
                if count > 5 and debug:
                    break
            if len(section[1]) > 0:
                section[0].href = section[1][0].file_name
            book.toc.append(section)
        return 0

    def add_images (self):
        book = self.book
        for root, dirs, files in os.walk(gonglue.IMAGES):
            for fn in files:
                filename = os.path.join(root, fn)
                extname = os.path.splitext(fn)[1].lower()
                if extname == '.md':
                    continue
                if fn == 'style.css':
                    continue
                srcname = os.path.relpath(filename, gonglue.IMAGES)
                srcname = srcname.replace('\\', '/')
                srcname = f'images/{srcname}'
                mimetype = gonglue.guess_mimetype(filename)
                item = epub.EpubItem(file_name=srcname, media_type=mimetype)
                with open(filename, 'rb') as f:
                    item.content = f.read()
                if extname == '.css':
                    item.content += b'\n\n'
                book.add_item(item)
                print('+', srcname, mimetype)
        name = os.path.join(gonglue.PROJECT, 'images/style_epub.css')
        item = epub.EpubItem(uid = "style_default", file_name = 'style/default.css', media_type='text/css')
        item.content = gonglue.read_file_content(name)
        book.add_item(item)
        self.css_epub = item
        name = os.path.join(gonglue.PROJECT, 'images/style_nav.css')
        item = epub.EpubItem(uid = "style_nav", file_name = 'style/nav.css', media_type='text/css')
        item.content = gonglue.read_file_content(name)
        book.add_item(item)
        self.css_nav = item
        return 0

    def build (self):
        print('building epub...')
        book = self.book
        # toc: table of content (index menu)
        book.add_item(epub.EpubNcx())
        # navi pages
        book.add_item(epub.EpubNav())
        opts = {}
        opts['epub3_landmark'] = False
        opts['epub3_pages'] = False
        opts['epub3_pages'] = False
        epub.write_epub(f'{gonglue.BUILD}/GONGLUE.epub', book, opts)
        return 0



#----------------------------------------------------------------------
# testing suit
#----------------------------------------------------------------------
if __name__ == '__main__':
    def test1():
        gonglue.prepare()
        book = EpubBook()
        book.init()
        book.add_images()
        book.add_html(debug = 0)
        book.build()
        return 0
    test1()


