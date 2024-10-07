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
import io


#----------------------------------------------------------------------
# global variables
#----------------------------------------------------------------------
FILEDIR = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.abspath(os.path.join(FILEDIR, '..'))
GONGLUE = os.path.join(PROJECT, 'GONGLUE')
BUILD = os.path.join(PROJECT, 'build')
HTMLDIR = os.path.join(BUILD, 'html')
IMAGES = os.path.join(BUILD, 'images')


#----------------------------------------------------------------------
# fix encoding
#----------------------------------------------------------------------
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


#----------------------------------------------------------------------
# auto detect encoding and decode into a string
#----------------------------------------------------------------------
def string_decode(payload, encoding = None):
    content = None
    if payload is None:
        return None
    if hasattr(payload, 'read'):
        try: content = payload.read()
        except: pass
    else:
        content = payload
    if content is None:
        return None
    if isinstance(content, str):
        return content
    if not isinstance(payload, bytes):
        return str(payload)
    if content[:3] == b'\xef\xbb\xbf':
        return content[3:].decode('utf-8', 'ignore')
    elif encoding is not None:
        return content.decode(encoding, 'ignore')
    guess = [sys.getdefaultencoding(), 'utf-8']
    if sys.stdout and sys.stdout.encoding:
        guess.append(sys.stdout.encoding)
    try:
        import locale
        guess.append(locale.getpreferredencoding())
    except:
        pass
    visit = {}
    text = None
    for name in guess + ['gbk', 'ascii', 'latin1']:
        if name in visit:
            continue
        visit[name] = 1
        try:
            text = content.decode(name)
            break
        except:
            pass
    if text is None:
        text = content.decode('utf-8', 'ignore')
    return text


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
        t = os.path.join(GONGLUE, fn)
        file_list['*'][fn] = t
    return file_list


#----------------------------------------------------------------------
# read file binary
#----------------------------------------------------------------------
def read_file_binary(filename):
    with open(filename, 'rb') as f:
        return f.read()
    return None


#----------------------------------------------------------------------
# read file content
#----------------------------------------------------------------------
def read_file_content(filename, encoding = None):
    t = read_file_binary(filename)
    if t is not None:
        x = string_decode(t, encoding)
        if x is not None:
            x = x.replace('\r\n', '\n')
            return x
    return None


#----------------------------------------------------------------------
# read file title
#----------------------------------------------------------------------
def read_file_title(filename):
    title = ''
    if not os.path.isfile(filename):
        return os.path.splitext(os.path.basename(filename))[0]
    extname = os.path.splitext(filename)[-1].lower()
    content = read_file_content(filename)
    if content is not None:
        import io
        f = io.StringIO(content)
        for line in f:
            line = line.strip('\r\n\t ')
            if extname == '.md':
                if line.startswith('# '):
                    title = line.lstrip('# ')
                    break
            elif extname == '.txt':
                if line:
                    title = line.lstrip('# ')
                    break
            else:
                break
    if not title:
        title = os.path.splitext(os.path.basename(filename))[0]
    return title


#----------------------------------------------------------------------
# write file content
#----------------------------------------------------------------------
def write_file_content(filename, content):
    if isinstance(content, str):
        with open(filename, 'w', encoding = 'utf-8') as f:
            f.write(content)
    else:
        with open(filename, 'wb') as f:
            f.write(content)
    return 0


#----------------------------------------------------------------------
# json: load
#----------------------------------------------------------------------
def read_json(filename):
    import json
    content = read_file_content(filename)
    if content is not None:
        return json.loads(content)
    return None


#----------------------------------------------------------------------
# json: save
#----------------------------------------------------------------------
def write_json(filename, data):
    import json
    content = json.dumps(data, indent = 4, ensure_ascii = False)
    write_file_content(filename, content)
    return 0



#----------------------------------------------------------------------
# guess mimetype
#----------------------------------------------------------------------
def guess_mimetype(filename):
    extname = os.path.splitext(filename)[-1].lower()
    if extname in ('.jpg', '.jpeg'):
        return 'image/jpeg'
    elif extname == '.gif':
        return 'image/gif'
    elif extname == '.png':
        return 'image/png'
    elif extname == '.css':
        return 'text/css'
    elif extname in ('.html', '.htm'):
        return 'text/html'
    elif extname == '.txt':
        return 'text/plain'
    elif extname == '.md':
        return 'text/markdown'
    return 'application/octet-stream'



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
            t1 = dirname.encode('gbk', errors = 'ignore')
            t2 = fn.encode('gbk', errors = 'ignore')
            t3 = title.encode('gbk', errors = 'ignore')
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
# add target="_blank" to external links
#----------------------------------------------------------------------
def patch_markdown_html(html):
    import bs4
    soup = bs4.BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all('a'):
        if tag.has_attr('href'):
            href = tag['href']
            if href.startswith('http://') or href.startswith('https://'):
                tag['target'] = '_blank'
    return str(soup)


#----------------------------------------------------------------------
# default template
#----------------------------------------------------------------------
TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title><!--TITLE--></title>
<!--STYLE-->
<!--HEADER-->
</head>
<body>
<!--BODYHEAD-->
<!--CONTENT-->
<!--BODYFOOT-->
</body>
</html>
'''

#----------------------------------------------------------------------
# convert files
#----------------------------------------------------------------------
def convert(srcname, template, htmlfile, footer = None, css = None):
    style = ''
    if css:
        style = f'<link rel="stylesheet" href="{css}">'
    if os.path.splitext(srcname)[-1].lower() == '.md':
        import markdown
        text = read_file_content(srcname)
        text += '\n'
        if footer:
            text += '\n' + footer
        title = read_file_title(srcname)
        extensions = ['markdown.extensions.extra']
        extensions.append('markdown.extensions.tables')
        extensions.append('markdown.extensions.toc')
        extensions.append('markdown.extensions.fenced_code')
        extensions.append('markdown.extensions.tables')
        extensions.append('markdown.extensions.admonition')
        extensions.append('markdown.extensions.wikilinks')
        extensions.append('markdown.extensions.nl2br')
        content = markdown.markdown(text, extensions = extensions)
        final = template.replace('<!--TITLE-->', title)
        final = final.replace('<!--CONTENT-->', content)
        final = final.replace('<!--STYLE-->', style)
        final = patch_markdown_html(final)
        if htmlfile:
            with open(htmlfile, 'wt', encoding='utf-8') as f:
                f.write(final)
        return final
    title = ''
    content = read_file_content(srcname)
    sio = io.StringIO(content)
    for line in sio:
        line = line.rstrip('\r\n\t ')
        if not line:
            continue
        title = line.lstrip('# ')
        break
    text = sio.read()
    text += '\n'
    if not title:
        title = os.path.splitext(os.path.basename(srcname))[0]
    if footer:
        text += '\n' + footer
    content = text2html(text)
    content = '<h1>' + title + '</h1>\n\n' + content
    final = template.replace('<!--TITLE-->', title)
    final = final.replace('<!--CONTENT-->', content)
    final = final.replace('<!--STYLE-->', style)
    if htmlfile:
        with open(htmlfile, 'wt', encoding='utf-8') as f:
            f.write(final)
    return final


#----------------------------------------------------------------------
# compile to html
#----------------------------------------------------------------------
def compile_to_html(verbose = False):
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
            if os.path.splitext(filename)[-1].lower() == '.md':
                css = '../../images/style_md.css'
            else:
                css = '../../images/style_txt.css'
            if verbose:
                print(f'Generating {relname} ...')
            t = convert(srcname, TEMPLATE, outname, None, css)
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
            if verbose:
                print(f'Generating {relname} ...')
            css = '../images/style_top.css'
            t = convert(srcname, TEMPLATE, outname, footer, css)
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
# copy images
#----------------------------------------------------------------------
def copy_images():
    import shutil
    if os.path.isdir(IMAGES):
        shutil.rmtree(IMAGES)
    shutil.copytree(os.path.join(PROJECT, 'images'), IMAGES)
    return 0


#----------------------------------------------------------------------
# prepare work
#----------------------------------------------------------------------
def prepare():
    print('Initializing ...')
    clear_html()
    print('Copying images ...')
    copy_images()
    print('Compiling to html ...')
    compile_to_html()
    print('Ready to proceed.')
    print('')
    sys.stdout.flush()
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
        # copy_images()
        return 0
    test5()



