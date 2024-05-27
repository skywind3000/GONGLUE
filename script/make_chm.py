#! /usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# make_chm.py - new chm generator using chmcmd
#
# Created by skywind on 2024/05/23
# Last Modified: 2024/05/23 17:26:08
#
#======================================================================
import sys
import time
import os
import codecs
import bs4
import gonglue


#----------------------------------------------------------------------
# internal
#----------------------------------------------------------------------
DOC = os.path.join(gonglue.BUILD, 'doc')


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
                tag['src'] = '../images/' + src[pos + 8:]
    for tag in soup.find_all('link'):
        href = tag.get('href')
        if href:
            pos = href.find('/images/')
            if pos >= 0:
                tag['href'] = '../images/' + href[pos + 8:]
    for tag in soup.find_all('a'):
        href = tag.get('href')
        if href:
            if href.startswith('http://') or href.startswith('https://'):
                tag['target'] = '_blank'
    html = str(soup)
    return html


#----------------------------------------------------------------------
# chm book
#----------------------------------------------------------------------
class ChmBook (object):

    def __init__ (self):
        self.htmls = gonglue.list_html()

    def prepare (self):
        self.names = {}
        self.title = {}
        self.reverse = {}
        if not os.path.exists(DOC):
            os.makedirs(DOC)
        self.names['html/INTRO.html'] = 'doc/c0.html'
        self.__patch_html('html/INTRO.html', 'doc/c0.html')
        index = 0
        for dirname in self.htmls:
            if dirname == '*':
                for fn in self.htmls[dirname]:
                    if fn == 'INTRO.html':
                        continue
                    index += 1
                    srcname = f'html/{fn}'
                    dstname = f'doc/c{index}.html'
                    self.names[srcname] = dstname
                    self.title[srcname] = self.htmls[dirname][fn]
                    self.reverse[dstname] = srcname
                    self.__patch_html(srcname, dstname)
            else:
                for fn in self.htmls[dirname]:
                    index += 1
                    srcname = f'html/{dirname}/{fn}'
                    dstname = f'doc/c{index}.html'
                    self.names[srcname] = dstname
                    self.title[srcname] = self.htmls[dirname][fn]
                    self.reverse[dstname] = srcname
                    self.__patch_html(srcname, dstname)
        return 0

    def __patch_html (self, srcname, dstname):
        t = gonglue.BUILD
        # print(f'  {srcname} -> {dstname}')
        content = gonglue.read_file_content(os.path.join(t, srcname))
        html = patch_html(content)
        open(os.path.join(t, dstname), 'w', encoding = 'utf-8').write(html)
        return 0

    def create_hhp (self, enable_search = True):
        hhp = os.path.join(gonglue.BUILD, 'chm.hhp')
        version = time.strftime('%Y-%m-%d')
        with open(hhp, 'w', encoding = 'gbk') as f:
            f.write('[OPTIONS]\n')
            f.write('Binary Index=Yes\n')
            f.write('Binary TOC=Yes\n')
            f.write('Compatibility=1.1 or later\n')
            f.write('Compiled file=GONGLUE.chm\n')
            f.write('Contents file=chm.hhc\n')
            f.write('Index file=chm.hhk\n')
            # f.write('Default Window=Main\n')
            f.write('Default Window=MyWindow\n')
            f.write('Default topic=doc\\c0.html\n')
            f.write('Display compile progress=Yes\n')
            if enable_search:
                f.write('Full-text search=Yes\n')
            else:
                f.write('Full-text search=No\n')
            f.write('Language=0x804 Chinese (Simplified, PRC)\n')
            f.write(f'Title=游戏攻略秘籍汇编（{version}）\n')
            f.write('\n')
            f.write('[WINDOWS]\n')
            w = f'"游戏攻略秘籍汇编（{version})",'
            if enable_search:
                w += r'"chm.hhc","chm.hhk","doc\c0.html","doc\c0.html",,,,,0x63520,,0x384e,[0,0,500,400],,,,,,,0'
            else:
                w += r'"chm.hhc","chm.hhk","doc\c0.html","doc\c0.html",,,,,0x43120,,0x384e,[0,0,500,400],,,,,,,0'               
            f.write(f'MyWindow={w}\n')
            f.write('\n')
            f.write('[FILES]\n')
            for dirname in self.htmls:
                if dirname != '*':
                    for fn in self.htmls[dirname]:
                        srcname = f'html/{dirname}/{fn}'
                        dstname = self.names[srcname]
                        f.write(dstname.replace('/', '\\') + '\n')
                else:
                    for fn in self.htmls['*']:
                        srcname = f'html/{fn}'
                        dstname = self.names[srcname]
                        f.write(dstname.replace('/', '\\') + '\n')
            for root, dirs, files in os.walk(gonglue.IMAGES):
                for fn in files:
                    img = os.path.join(root, fn)
                    img = os.path.relpath(img, gonglue.IMAGES)
                    f.write(f'images\\{img}\n')
            f.write('\n')
            f.write('[INFOTYPES]\n')
            f.write('\n')
            f.write('[ALIAS]\n')
            f.write('\n')
            f.write('[MAP]\n')
            f.write('\n')
        return hhp

    def create_hhc (self):
        hhc = os.path.join(gonglue.BUILD, 'chm.hhc')
        with open(hhc, 'w', encoding = 'gbk') as f:
            f.write('<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">\n')
            f.write('<HTML>\n')
            f.write('<HEAD>\n')
            f.write('<meta name="GENERATOR" content="Microsoft&reg; HTML Help Workshop 4.1">\n')
            f.write('<!-- Sitemap 1.0 -->\n')
            f.write('</HEAD>\n')
            f.write('<BODY>\n')
            f.write('<OBJECT type="text/site properties">\n')
            f.write('  <param name="ImageType" value="Folder">\n')
            f.write('</OBJECT>\n')
            f.write('<UL>\n')
            if '*' in self.htmls:
                htmls = self.htmls['*']
                for fn in htmls:
                    title = htmls[fn]
                    srcname = f'html/{fn}'
                    dstname = self.names[srcname].replace('/', '\\')
                    f.write('<LI><OBJECT type="text/sitemap">\n')
                    f.write(f'  <param name="Name" value="{title}">\n')
                    f.write(f'  <param name="Local" value="{dstname}">\n')
                    f.write('</OBJECT>\n')
            for dirname in self.htmls:
                if dirname == '*':
                    continue
                htmls = self.htmls[dirname]
                f.write('<LI><OBJECT type="text/sitemap">\n')
                f.write(f'  <param name="Name" value="{dirname}">\n')
                f.write('</OBJECT>\n')
                f.write('<UL>\n')
                for fn in htmls:
                    title = htmls[fn]
                    srcname = f'html/{dirname}/{fn}'
                    dstname = self.names[srcname].replace('/', '\\')
                    f.write('<LI><OBJECT type="text/sitemap">\n')
                    f.write(f'  <param name="Name" value="{title}">\n')
                    f.write(f'  <param name="Local" value="{dstname}">\n')
                    f.write('</OBJECT>\n')
                f.write('</UL>\n')
            f.write('</UL>\n')
            f.write('</BODY>\n')
            f.write('</HTML>\n')
        return hhc
    
    def create_hhk (self):
        hhk = os.path.join(gonglue.BUILD, 'chm.hhk')
        with open(hhk, 'w', encoding = 'gbk') as f:
            f.write('<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">\n')
            f.write('<HTML>\n')
            f.write('<HEAD>\n')
            f.write('<meta name="GENERATOR" content="Microsoft&reg; HTML Help Workshop 4.1">\n')
            f.write('<!-- Sitemap 1.0 -->\n')
            f.write('</HEAD>\n')
            f.write('<BODY>\n')
            f.write('<UL>\n')
            for dirname in self.htmls:
                if dirname == '*':
                    continue
                htmls = self.htmls[dirname]
                for fn in htmls:
                    title = htmls[fn]
                    srcname = f'html/{dirname}/{fn}'
                    dstname = self.names[srcname].replace('/', '\\')
                    f.write('<LI><OBJECT type="text/sitemap">\n')
                    f.write(f'  <param name="Name" value="{title}">\n')
                    f.write(f'  <param name="Local" value="{dstname}">\n')
                    f.write('</OBJECT>\n')
            f.write('</UL>\n')
            f.write('</BODY>\n')
            f.write('</HTML>\n')
        return 0

    def build (self):
        os.chdir(gonglue.BUILD)
        cmd = 'chmcmd chm.hhp'
        os.system(cmd)
        return 0


#----------------------------------------------------------------------
# build chm
#----------------------------------------------------------------------
def build_chm():
    gonglue.prepare()
    book = ChmBook()
    print('Patching html ...')
    book.prepare()
    print('Creating hhp/hhc/hhk ...')
    book.create_hhp(enable_search = 0)
    book.create_hhc()
    book.create_hhk()
    print('Building chm ...')
    print('')
    sys.stdout.flush()
    book.build()
    return 0


#----------------------------------------------------------------------
# testing suit
#----------------------------------------------------------------------
if __name__ == '__main__':
    def test1():
        build_chm()
        return 0
    def test2():
        book = ChmBook()
        print('Creating hhp/hhc/hhk ...')
        book.prepare()
        book.create_hhp(enable_search = 0)
        book.create_hhc()
        book.create_hhk()
        book.build()
        return 0
    test1()




