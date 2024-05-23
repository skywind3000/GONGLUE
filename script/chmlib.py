#! /usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# chmlib.py - 
#
# Created by skywind on 2024/05/23
# Last Modified: 2024/05/23 16:44:35
#
#======================================================================
import sys
import os


#----------------------------------------------------------------------
# chapter
#----------------------------------------------------------------------
class Chapter (object):

    def __init__ (self, title, content):
        self.title = title
        self.content = content
        self.uuid = None

    def __str__ (self):
        return self.title


#----------------------------------------------------------------------
# ebook
#----------------------------------------------------------------------
class EBook (object):

    def __init__ (self):
        self.title = ''
        self.author = ''
        self.chapters = []
        self.toc = []

    def reset (self):
        self.chapters = []
        self.toc = []

    def add_chapter (self, title, content):
        c = Chapter(title, content)
        c.uuid = len(self.chapters)
        self.chapters.append(c)

