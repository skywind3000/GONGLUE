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
        uuid = 'GAMEGUIDE-LW-' + time.strftime('%Y%m%d%H%M%S')
        epub.set_identifier(uuid)
        epub.set_title('Game Guide')
        epub.add_author('skywind')
        epub.set_language('zh')

    def add_html (self):
        epub = self.epub
        if '*' in self.htmls:
            for fn in self.htmls['*']:
                title = self.htmls['*'][fn]
                srcname = f'html/{fn}'
                print(srcname)
                filename = os.path.join(gonglue.BUILD, srcname)
                item = ebooklib.epub.EpubHtml(title=title, file_name=srcname)
                item.content = gonglue.read_file_content(filename)
                epub.add_item(item)
                epub.toc.append(item)
        for dirname in self.htmls:
            count = 0
            if dirname == '*':
                continue
            section = [ebooklib.epub.Section(dirname), []]
            for fn in self.htmls[dirname]:
                title = self.htmls[dirname][fn]
                srcname = f'html/{dirname}/{fn}'
                print(srcname)
                filename = os.path.join(gonglue.BUILD, srcname)
                item = ebooklib.epub.EpubHtml(title=title, file_name=srcname)
                item.content = gonglue.read_file_content(filename)
                epub.add_item(item)
                section[1].append(item)
                count += 1
                if count > 5:
                    break
            section[1] = tuple(section[1])
            epub.toc.append(tuple(section))
        return 0

    def add_images (self):
        epub = self.epub
        for root, dirs, files in os.walk(gonglue.IMAGES):
            for fn in files:
                filename = os.path.join(root, fn)
                srcname = os.path.relpath(filename, gonglue.IMAGES)
                srcname = f'images/{srcname}'
                mimetype = gonglue.guess_mimetype(filename)
                item = ebooklib.epub.EpubItem(file_name=srcname, media_type=mimetype)
                with open(filename, 'rb') as f:
                    item.content = f.read()
                epub.add_item(item)
                print('+', srcname, mimetype)
        return 0

    def build (self):
        print('building epub...')
        epub = self.epub
        # toc: table of content (index menu)
        epub.add_item(ebooklib.epub.EpubNcx())
        # navi pages
        # epub.add_item(ebooklib.epub.EpubNav())
        epub.spine = ['nav'] + self.epub.toc
        epub.add_item(ebooklib.epub.EpubCover())
        ebooklib.epub.write_epub(f'{gonglue.BUILD}/GONGLUE.epub', epub, {})
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
        book.build()
        return 0
    test1()


