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
# testing suit
#----------------------------------------------------------------------
if __name__ == '__main__':
    def test1():
        t = fetch('http://www.baidu.com/')
        print(t)
        return 0
    def test2():
        return 0
    test2()


