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
import ebooklib.epub
import gonglue


#----------------------------------------------------------------------
# Epub Book
#----------------------------------------------------------------------
class EpubBook (object):

    def __init__ (self):
        self.htmls = gonglue.list_html()
        self.epub = ebooklib.epub.EpubBook()

    def init (self):
        epub = self.epub
        epub.set_identifier('GAMEGUIDE20240524')
        epub.set_title('Game Guide')
        epub.add_author('skywind')
        epub.set_language('zh')

    def add_html (self):
        epub = self.epub
        for dirname in self.htmls:
            count = 0
            for fn in self.htmls[dirname]:
                title = self.htmls[dirname][fn]
                if dirname != '*':
                    srcname = f'html/{dirname}/{fn}'
                else:
                    srcname = f'html/{fn}'
                print(srcname)
                filename = os.path.join(gonglue.BUILD, srcname)
                item = ebooklib.epub.EpubHtml(title=title, file_name=srcname)
                item.content = gonglue.read_file_content(filename)
                epub.add_item(item)
                epub.toc.append(item)
                count += 1
                if count > 10:
                    break
        return 0

    def add_images (self):
        epub = self.epub
        for root, dirs, files in os.walk(gonglue.IMAGES):
            for fn in files:
                filename = os.path.join(root, fn)
                srcname = os.path.relpath(filename, gonglue.IMAGES)
                mimetype = gonglue.guess_mimetype(filename)
                item = ebooklib.epub.EpubItem(file_name=srcname, media_type=mimetype)
                with open(filename, 'rb') as f:
                    item.content = f.read()
                epub.add_item(item)
                print('+', srcname, mimetype)
        return 0



#----------------------------------------------------------------------
# testing suit
#----------------------------------------------------------------------
if __name__ == '__main__':
    def test1():
        book = EpubBook()
        book.init()
        book.add_html()
        book.add_images()
        return 0
    test1()


