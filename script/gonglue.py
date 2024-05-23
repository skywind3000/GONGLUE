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
import time
import os


#----------------------------------------------------------------------
# global variables
#----------------------------------------------------------------------
FILEDIR = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.abspath(os.path.join(FILEDIR, '..'))
GONGLUE = os.path.join(PROJECT, 'GONGLUE')
BUILD = os.path.join(PROJECT, 'build')
HTMLDIR = os.path.join(BUILD, 'html')


#----------------------------------------------------------------------
# list text files
#----------------------------------------------------------------------
def list_text():
    file_list = {}
    for dirname in os.listdir(GONGLUE):
        if not os.path.isdir(os.path.join(GONGLUE, dirname)):
            continue
        file_list[dirname] = {}
        for filename in os.listdir(os.path.join(GONGLUE, dirname)):
            parts = os.path.splitext(filename)
            if parts[-1].lower() in ('.txt', '.md'):
                t = os.path.join(GONGLUE, dirname, filename)
                file_list[dirname][filename] = t
    for fn in os.listdir(GONGLUE):
        parts = os.path.splitext(fn)
        if parts[1].lower() not in ('.txt', '.md'):
            continue
        if '*' not in file_list:
            file_list['*'] = {}
        file_list['*'][fn] = os.path.join(GONGLUE, fn)
    return file_list


#----------------------------------------------------------------------
# read file title
#----------------------------------------------------------------------
def read_file_title(filename):
    title = ''
    if not os.path.isfile(filename):
        return os.path.splitext(os.path.basename(filename))[0]
    with open(filename, 'r', encoding = 'utf-8', errors = 'ignore') as f:
        for line in f:
            line = line.strip('\r\n\t ')
            if line:
                title = line.lstrip('# ')
                break
    if not title:
        title = os.path.splitext(os.path.basename(filename))[0]
    return title


#----------------------------------------------------------------------
# list htmls
#----------------------------------------------------------------------
def list_html():
    html_files = {}
    for dirname in os.listdir(HTMLDIR):
        if not os.path.isdir(os.path.join(HTMLDIR, dirname)):
            continue
        html_files[dirname] = {}
        for filename in os.listdir(os.path.join(HTMLDIR, dirname)):
            if filename.endswith('.html'):
                parts = os.path.splitext(filename)
                src = os.path.join(GONGLUE, dirname, parts[0] + '.md')
                if not os.path.isfile(src):
                    src = os.path.join(GONGLUE, dirname, parts[0] + '.txt')
                if not os.path.isfile(src):
                    raise FileNotFoundError(src)
                title = read_file_title(src)
                html_files[dirname][filename] = title
    for fn in os.listdir(HTMLDIR):
        parts = os.path.splitext(fn)
        if parts[-1].lower() != '.html':
            continue
        if '*' not in html_files:
            html_files['*'] = {}
        src = os.path.join(GONGLUE, parts[0] + '.md')
        if not os.path.isfile(src):
            src = os.path.join(GONGLUE, parts[0] + '.txt')
        if not os.path.isfile(src):
            raise FileNotFoundError(src)
        title = read_file_title(src)
        html_files['*'][fn] = title
    sorted_array = []
    for dirname in html_files:
        for fn, title in html_files[dirname].items():
            t1 = dirname.encode('gbk')
            t2 = fn.encode('gbk')
            t3 = title.encode('gbk')
            sorted_array.append((t1, t2, t3))
    sorted_array.sort()
    html_files = {}
    for t1, t2, t3 in sorted_array:
        dirname = t1.decode('gbk')
        filename = t2.decode('gbk')
        title = t3.decode('gbk')
        if dirname not in html_files:
            html_files[dirname] = {}
        html_files[dirname][filename] = title
    return html_files


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
    return '\n'.join(output)


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
def convert(srcname, template, htmlfile, footer = None):
    title = ''
    with open(srcname, 'r', encoding='utf-8', errors = 'ignore') as f:
        for line in f:
            line = line.rstrip('\r\n\t ')
            if not line:
                continue
            title = line.lstrip('# ')
            break
        text = f.read()
    text += '\n'
    if not title:
        title = os.path.splitext(os.path.basename(srcname))[0]
    if footer:
        text += '\n' + footer
    content = text2html(text)
    content = '<h1>' + title + '</h1>\n\n' + content
    final = template.replace('<!--TITLE-->', title)
    final = final.replace('<!--CONTENT-->', content)
    if htmlfile:
        with open(htmlfile, 'wt', encoding='utf-8') as f:
            f.write(final)
    return final


#----------------------------------------------------------------------
# compile to html
#----------------------------------------------------------------------
def compile_to_html():
    file_list = list_text()
    for dirname in file_list:
        if dirname == '*':
            continue
        target = os.path.join(HTMLDIR, dirname)
        if not os.path.isdir(target):
            os.makedirs(target, exist_ok = True)
        for filename in file_list[dirname]:
            srcname = file_list[dirname][filename]
            outname = os.path.join(target, os.path.splitext(filename)[0] + '.html')
            relname = os.path.relpath(outname, BUILD)
            print(f'Generating {relname} ...')
            t = convert(srcname, TEMPLATE, outname)
            if 0:
                print(t)
                sys.exit(1)
    if '*' in file_list:
        target = HTMLDIR
        footer = time.strftime('Created on: %Y-%m-%d %H:%M:%S')
        footer = f'\n{footer}\n'
        if not os.path.isdir(target):
            os.makedirs(target, exist_ok = True)
        for filename in file_list['*']:
            srcname = file_list['*'][filename]
            outname = os.path.join(target, os.path.splitext(filename)[0] + '.html')
            relname = os.path.relpath(outname, BUILD)
            print(f'Generating {relname} ...')
            t = convert(srcname, TEMPLATE, outname, footer)
    return 0


#----------------------------------------------------------------------
# remove html folder
#----------------------------------------------------------------------
def clear_html():
    import shutil
    if os.path.isdir(HTMLDIR):
        shutil.rmtree(HTMLDIR)
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
        file_list = list_text()
        for dirname in file_list:
            for filename in file_list[dirname]:
                srcname = file_list[dirname][filename]
                print(f'Converting {srcname} ...')
                convert(srcname, TEMPLATE, None)
        return 0
    def test3():
        compile_to_html()
        return 0
    def test4():
        html_files = list_html()
        import pprint
        pprint.pprint(html_files)
        return 0
    def test5():
        return 0
    test5()



