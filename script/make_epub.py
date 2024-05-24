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
from ebooklib import epub
import gonglue


#----------------------------------------------------------------------
# Epub Book
#----------------------------------------------------------------------
class EpubBook (object):

    def __init__ (self):
        self.htmls = gonglue.list_html()
        self.book = epub.EpubBook()

    def init (self):
        book = self.book
        uuid = 'GAMEGUIDE-LW-' + time.strftime('%Y%m%d%H%M%S')
        book.set_identifier(uuid)
        book.set_title('Game Guide')
        book.add_author('skywind')
        book.set_language('zh')
        book.toc = []
        book.spine = []

    def add_html (self):
        book = self.book
        if '*' in self.htmls:
            for fn in self.htmls['*']:
                title = self.htmls['*'][fn]
                srcname = f'html/{fn}'
                print(srcname)
                filename = os.path.join(gonglue.BUILD, srcname)
                item = epub.EpubHtml(title=title, file_name=srcname)
                item.content = gonglue.read_file_content(filename)
                book.add_item(item)
                book.toc.append(item)
                book.spine.append(item)
        for dirname in self.htmls:
            count = 0
            if dirname == '*':
                continue
            section = [epub.Section(dirname), []]
            for fn in self.htmls[dirname]:
                title = self.htmls[dirname][fn]
                srcname = f'html/{dirname}/{fn}'
                print(srcname)
                filename = os.path.join(gonglue.BUILD, srcname)
                item = epub.EpubHtml(title=title, file_name=srcname)
                item.content = gonglue.read_file_content(filename)
                book.add_item(item)
                book.spine.append(item)
                section[1].append(item)
                count += 1
                if count > 5 and 1:
                    break
            section[1] = tuple(section[1])
            book.toc.append(tuple(section))
        return 0

    def add_images (self):
        book = self.book
        for root, dirs, files in os.walk(gonglue.IMAGES):
            for fn in files:
                filename = os.path.join(root, fn)
                srcname = os.path.relpath(filename, gonglue.IMAGES)
                srcname = f'images/{srcname}'
                mimetype = gonglue.guess_mimetype(filename)
                item = epub.EpubItem(file_name=srcname, media_type=mimetype)
                with open(filename, 'rb') as f:
                    item.content = f.read()
                book.add_item(item)
                print('+', srcname, mimetype)
        name = os.path.join(gonglue.PROJECT, 'images/style_epub.css')
        item = epub.EpubItem(uid = "style_default", file_name = 'style/default.css', media_type='text/css')
        item.content = gonglue.read_file_content(name)
        book.add_item(item)
        return 0

    def add_cover (self):
        book = self.book
        book.add_item(epub.EpubCover())
        return 0

    def build (self):
        print('building epub...')
        book = self.book
        # toc: table of content (index menu)
        book.add_item(epub.EpubNcx())
        # navi pages
        book.add_item(epub.EpubNav())
        epub.write_epub(f'{gonglue.BUILD}/GONGLUE.epub', book, {})
        return 0



#----------------------------------------------------------------------
# testing suit
#----------------------------------------------------------------------
if __name__ == '__main__':
    def test1():
        book = EpubBook()
        book.init()
        book.add_images()
        book.add_html()
        book.add_cover()
        book.build()
        return 0
    test1()


