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
import os
import gonglue


#----------------------------------------------------------------------
# chm book
#----------------------------------------------------------------------
class ChmBook (object):

    def __init__ (self):
        self.htmls = gonglue.list_html()

    def create_hhp (self):
        hhp = os.path.join(gonglue.BUILD, 'chm.hhp')
        with open(hhp, 'w', encoding = 'utf-8') as f:
            f.write('[OPTIONS]\n')
            f.write('Binary Index=Yes\n')
            f.write('Binary TOC=Yes\n')
            f.write('Compatibility=1.1 or later\n')
            f.write('Compiled file=gonglue.chm\n')
            f.write('Contents file=chm.hhc\n')
            f.write('Index file=chm.hhk\n')
            f.write('Default Window=Main\n')
            f.write('Default topic=html\\INTRO.html\n')
            f.write('Display compile progress=Yes\n')
            f.write('Full-text search=No\n')
            f.write('Language=0x804 Chinese (Simplified, PRC)\n')
            f.write('Title=游戏攻略秘籍大全\n')
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
        with open(hhc, 'w', encoding = 'utf-8') as f:
            f.write('<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">\n')
            f.write('<HTML>\n')
            f.write('<HEAD>\n')
            f.write('<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">\n')
            f.write('</HEAD>\n')
            f.write('<BODY>\n')
            f.write('<OBJECT type="text/site properties">\n')
            f.write('  <param name="ImageType" value="Folder">\n')
            f.write('</OBJECT>\n')
            f.write('<UL>\n')
            for dirname in self.htmls:
                if dirname != '*':
                    f.write(f'<LI><OBJECT type="text/sitemap">\n')
                    f.write(f'  <param name="Name" value="{dirname}">\n')
                    f.write(f'</OBJECT>\n')
                    f.write('<UL>\n')
                    for fn in self.htmls[dirname]:
                        title = gonglue.read_html_title(dirname, fn)
                        f.write(f'<LI><OBJECT type="text/sitemap">\n')
                        f.write(f'  <param name="Name" value="{title}">\n')
                        f.write(f'  <param name="Local" value="html\\{dirname}\\{fn}">\n')
                        f.write('</OBJECT>\n')
                    f.write('</UL>\n')
                else:
                    for fn in self.htmls['*']:
                        title = gonglue.read_html_title('*', fn)
                        f.write(f'<LI><OBJECT type="text/sitemap">\n')
                        f.write(f'  <param name="Name" value="{title}">\n')
                        f.write(f'  <param name="Local" value="html\\{fn}">\n')
                        f.write('</OBJECT>\n')
            f.write('</UL>\n')
            f.write('</BODY>\n')
            f.write('</HTML>\n')
        return hhc


#----------------------------------------------------------------------
# testing suit
#----------------------------------------------------------------------
if __name__ == '__main__':
    def test1():
        book = ChmBook()
        book.create_hhp()
        return 0
    test1()



