#! /usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# make_chm.py - 
#
# Created by skywind on 2024/05/23
# Last Modified: 2024/05/23 17:26:08
#
#======================================================================
import sys
import time
import os
import codecs
import gonglue


#----------------------------------------------------------------------
# chm book
#----------------------------------------------------------------------
class ChmBook (object):

    def __init__ (self):
        self.htmls = gonglue.list_html()

    def create_hhp (self):
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
            f.write('Default topic=html\\INTRO.html\n')
            f.write('Display compile progress=Yes\n')
            f.write('Full-text search=Yes\n')
            f.write('Language=0x804 Chinese (Simplified, PRC)\n')
            f.write(f'Title=游戏攻略秘籍汇编（{version}）\n')
            f.write('\n')
            f.write('[WINDOWS]\n')
            w = f'"游戏攻略秘籍汇编（{version})",'
            w += '"chm.hhc","chm.hhk","html\\INTRO.html","html\\INTRO.html",,,,,0x63520,,0x384e,[0,0,640,400],,,,,,,0'
            f.write(f'MyWindow={w}\n')
            f.write('\n')
            f.write('[FILES]\n')
            for dirname in self.htmls:
                if dirname != '*':
                    for fn in self.htmls[dirname]:
                        f.write(f'html\\{dirname}\\{fn}\n')
                else:
                    for fn in self.htmls['*']:
                        f.write(f'html\\{fn}\n')
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
                    f.write('<LI><OBJECT type="text/sitemap">\n')
                    f.write(f'  <param name="Name" value="{title}">\n')
                    f.write(f'  <param name="Local" value="html\\{fn}">\n')
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
                    f.write('<LI><OBJECT type="text/sitemap">\n')
                    f.write(f'  <param name="Name" value="{title}">\n')
                    f.write(f'  <param name="Local" value="html\\{dirname}\\{fn}">\n')
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
                    f.write('<LI><OBJECT type="text/sitemap">\n')
                    f.write(f'  <param name="Name" value="{title}">\n')
                    f.write(f'  <param name="Local" value="html\\{dirname}\\{fn}">\n')
                    f.write('</OBJECT>\n')
            f.write('</UL>\n')
            f.write('</BODY>\n')
            f.write('</HTML>\n')
        return 0

    def build (self):
        hhp = os.path.join(gonglue.BUILD, 'chm.hhp')
        cmd = f'hhc {hhp}'
        os.system(cmd)
        return 0


#----------------------------------------------------------------------
# testing suit
#----------------------------------------------------------------------
if __name__ == '__main__':
    def test1():
        book = ChmBook()
        book.create_hhp()
        book.create_hhc()
        book.create_hhk()
        book.build()
        return 0
    test1()



