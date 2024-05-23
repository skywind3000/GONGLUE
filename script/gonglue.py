#! /usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# gonglue.py - 
#
# Created by skywind on 2024/05/23
# Last Modified: 2024/05/23 14:57:24
#
#======================================================================
import sys
import os


#----------------------------------------------------------------------
# global variables
#----------------------------------------------------------------------
FILEDIR = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.abspath(os.path.join(FILEDIR, '..'))
GONGLUE = os.path.join(PROJECT, 'GONGLUE')
BUILD = os.path.join(PROJECT, 'build')


#----------------------------------------------------------------------
# list text files
#----------------------------------------------------------------------
def list_text():
    file_list = {}
    for dirname in os.listdir(GONGLUE):
        file_list[dirname] = {}
        for filename in os.listdir(os.path.join(GONGLUE, dirname)):
            if filename.endswith('.txt'):
                t = os.path.join(GONGLUE, dirname, filename)
                file_list[dirname][filename] = t
    return file_list


#----------------------------------------------------------------------
# to html
#----------------------------------------------------------------------
def text2html(text):
    import html
    output = []
    for line in text.split('\n'):
        line = line.rstrip('\r\n\t ')
        if not line:
            output.append('<p></p>')
            continue
        t = html.escape(line)
        output.append(f'<p>{t}</p>')
    return ''.join(output)


#----------------------------------------------------------------------
# default template
#----------------------------------------------------------------------
TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title><!--TITLE--></title>
</head>
<body>
<!--CONTENT-->
</body>
</html>
'''

#----------------------------------------------------------------------
# convert files
#----------------------------------------------------------------------
def convert(srcname, template, htmlfile):
    with open(srcname, 'rt', encoding='utf-8', errors = 'ignore') as f:
        text = f.read()
    title = text.split('\n', 1)[0]
    if not title:
        title = os.path.splitext(os.path.basename(srcname))[0]
    content = text2html(text)
    final = template.replace('<!--TITLE-->', title)
    final = final.replace('<!--CONTENT-->', content)
    with open(htmlfile, 'wt', encoding='utf-8') as f:
        f.write(final)
    return 0


#----------------------------------------------------------------------
# compile to html
#----------------------------------------------------------------------
def compile_to_html():
    file_list = list_text()
    for dirname in file_list:
        target = os.path.join(BUILD, dirname)
        if not os.path.isdir(target):
            os.makedirs(target, exist_ok = True)
        for filename in file_list[dirname]:
            srcname = file_list[dirname][filename]
            outname = os.path.join(target, os.path.splitext(filename)[0] + '.html')
            convert(srcname, TEMPLATE, outname)
            print(f'generating {outname} ...')
    return 0


#----------------------------------------------------------------------
# testing suit
#----------------------------------------------------------------------
if __name__ == '__main__':
    def test1():
        import pprint
        file_list = list_text()
        pprint.pprint(file_list)
        return 0
    def test2():
        compile_to_html()
        return 0
    test2()



