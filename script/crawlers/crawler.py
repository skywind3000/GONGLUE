#! /usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# crawler.py - game guide crawler library
#
# Created by skywind on 2024/05/26
# Last Modified: 2024/05/26 04:53:07
#
#======================================================================
import sys
import time
import os


#----------------------------------------------------------------------
# internals
#----------------------------------------------------------------------
DIRNAME = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.abspath(os.path.join(DIRNAME, '../..'))
BUILD = os.path.join(PROJECT, 'build')
CACHE = os.path.join(PROJECT, '.cache')
SCRIPT = os.path.join(PROJECT, 'script')
CRAWLER = os.path.join(PROJECT, 'script/crawlers')


#----------------------------------------------------------------------
# LazyRequests
#----------------------------------------------------------------------
class LazyRequests (object):
    
    def __init__ (self):
        import threading
        self._pools = {}
        self._lock = threading.Lock()
        self._options = {}
        self._option = {}
    
    def __session_get (self, name):
        hr = None
        with self._lock:
            pset = self._pools.get(name, None)
            if pset:
                hr = pset.pop()
        return hr
    
    def __session_put (self, name, obj):
        with self._lock:
            pset = self._pools.get(name, None)
            if pset is None:
                pset = set()
                self._pools[name] = pset
            pset.add(obj)
        return True

    def request (self, name, url, data = None, post = False, header = None):
        import requests
        import copy
        s = self.__session_get(name)
        if not s:
            s = requests.Session()
        r = None
        option = self._options.get(name, {})
        argv = {}
        timeout = self._option.get('timeout', None)
        proxy = self._option.get('proxy', None)
        agent = self._option.get('agent', None)
        if 'timeout' in option:
            timeout = option.get('timeout')
        if 'proxy' in option:
            proxy = option['proxy']
        if proxy and isinstance(proxy, str):
            if proxy.startswith('socks5://'):
                proxy = 'socks5h://' + proxy[9:]
                proxy = {'http': proxy, 'https': proxy}
        if 'agent' in option:
            agent = option['agent']
        if timeout:
            argv['timeout'] = timeout
        if proxy:
            argv['proxies'] = proxy
        if header is None:
            header = {}
        else:
            header = copy.deepcopy(header)
        if agent:
            header['User-Agent'] = agent
        if header is not None:
            argv['headers'] = header
        if not post:
            if data is not None:
                argv['params'] = data
        else:
            # pylint: disable-next=else-if-used
            if data is not None:
                argv['data'] = data
        try:
            if not post:
                r = s.get(url, **argv)
            else:
                r = s.post(url, **argv)
        except requests.exceptions.ConnectionError:
            r = None
        except requests.exceptions.RetryError as e:
            r = requests.Response()
            r.status_code = -1
            r.text = 'RetryError'
            r.error = e
        except requests.exceptions.BaseHTTPError as e:
            r = requests.Response()
            r.status_code = -2
            r.text = 'BaseHTTPError'
            # pylint: disable-next=redefined-variable-type
            r.error = e
        except requests.exceptions.HTTPError as e:
            r = requests.Response()
            r.status_code = -3
            r.text = 'HTTPError'
            r.error = e
        except requests.exceptions.RequestException as e:
            r = requests.Response()
            r.status_code = -4
            r.error = e
        self.__session_put(name, s)
        return r

    def option (self, name, opt, value):
        if name is None:
            self._option[opt] = value
        else:
            if name not in self._options:
                self._options[name] = {}
            opts = self._options[name]
            opts[opt] = value
        return True

    def get (self, name, url, data = None, header = None):
        return self.request(name, url, data, False, header)

    def post (self, name, url, data = None, header = None):
        return self.request(name, url, data, True, header)

    def wget (self, name, url, data = None, post = False, header = None):
        r = self.request(name, url, data, post, header)
        if r is None:
            return -1, None
        if r.content:
            text = r.content.decode('utf-8', errors = 'ignore')
        else:
            text = r.text
        return r.status_code, text


#----------------------------------------------------------------------
# instances
#----------------------------------------------------------------------
lazy = LazyRequests()

lazy.option(None, 'timeout', 10)
lazy.option(None, 'proxy', None)
lazy.option(None, 'agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')


def fetch(url):
    code, text = lazy.wget(None, url)
    if code != 200:
        raise IOError(code, f'fetch failed({code}): {url}')
    return text


#----------------------------------------------------------------------
# functions
#----------------------------------------------------------------------
def read_file_content(filename):
    with open(filename, 'r', encoding = 'utf-8', errors = 'ignore') as f:
        return f.read()
    return None


#----------------------------------------------------------------------
# download file
#----------------------------------------------------------------------
def download(url, filename, skip = False):
    import requests
    if skip and os.path.exists(filename):
        # print(f'skip download: {filename}')
        return 1
    r: requests.Response = lazy.get(None, url)
    if r is None:
        raise IOError(-1, f'download failed: {url}')
    if r.status_code != 200:
        code = r.status_code
        raise IOError(code, f'download failed({code}): {url}')
    mime = r.headers.get('Content-Type', 'application/octet-stream')
    if mime.startswith('text/'):
        if r.content:
            text = r.content.decode('utf-8', errors = 'ignore')
        else:
            text = r.text
        with open(filename, 'w', encoding = 'utf-8') as f:
            f.write(text)
        print(f'download text: {filename}')
    else:
        with open(filename, 'wb') as f:
            f.write(r.content)
        print(f'download binary: {filename}')
    return 0


#----------------------------------------------------------------------
# ensure_dir 
#----------------------------------------------------------------------
def ensure_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return 0


#----------------------------------------------------------------------
# string_crc32: useful for changing remote image url to local file
#----------------------------------------------------------------------
def string_crc32(text):
    import zlib
    crc32 = zlib.crc32(text.encode('utf-8')) & 0xffffffff
    text = '%08x' % crc32
    return text.lower()


#----------------------------------------------------------------------
# image_local: change remote image url to local file
#----------------------------------------------------------------------
def image_local(url, dirname):
    name = string_crc32(url)
    ext = url.split('.')[-1].lower()
    if ext not in ('jpg', 'jpeg', 'png', 'gif', 'bmp'):
        ext = 'jpg'
    name = 'image_' + name + '.' + ext
    if dirname:
        name = os.path.join(dirname, name)
    return name.replace('\\', '/')


#----------------------------------------------------------------------
# 
#----------------------------------------------------------------------
def html_to_markdown(html, **options):
    import markdownify
    import bs4
    if isinstance(html, str):
        md = markdownify.markdownify(html, **options)
    elif isinstance(html, bs4.element.Tag):
        md = markdownify.MarkdownConverter(**options).convert_soup(html)
    else:
        raise TypeError('html_to_markdown: invalid type')
    return md


#----------------------------------------------------------------------
# merge empty lines
#----------------------------------------------------------------------
def merge_empty_lines(input_text):
    lines = input_text.split('\n')
    output_text = []
    for line in lines:
        if line.strip() == '':
            line = ''
        if line == '':
            if output_text and output_text[-1].strip() == '':
                continue
        output_text.append(line)
    return '\n'.join(output_text)


#----------------------------------------------------------------------
# localize_image: download images and change image url to local
#----------------------------------------------------------------------
def localize_image(root, dirname, prefix):
    import bs4
    assert isinstance(root, bs4.element.Tag)
    ensure_dir(dirname)
    for img in root.find_all('img'):
        src = img.get('src')
        if not src:
            continue
        if src.startswith('http://') or src.startswith('https://'):
            srcname = image_local(src, '')
            dstname = os.path.join(dirname, srcname)
            print('srcname', srcname)
            img.attrs['src'] = f'{prefix}{srcname}'
            if not os.path.isfile(dstname):
                print(f'downloading {dstname}')
                download(src, dstname)
            else:
                # print(f'already downloaded {filename}')
                pass
    return 0


#----------------------------------------------------------------------
# testing suit
#----------------------------------------------------------------------
if __name__ == '__main__':
    def test0():
        return 0
    def test1():
        t = fetch('http://www.baidu.com/')
        print(t)
        return 0
    def test2():
        download('http://www.baidu.com/', 'html/baidu.html')
        return 0
    def test3():
        print(string_crc32('http://www.baidu.com/'))
        return 0
    test3()


