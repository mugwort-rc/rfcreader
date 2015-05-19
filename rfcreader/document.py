# -*- coding: utf-8 -*-

import re

import six

class Document:
    def __init__(self):
        self.pages = []

    def append(self, page):
        self.pages.append(page)

    @property
    def pages(self):
        return self._pages

    @pages.setter
    def pages(self, pages):
        self._pages = pages

    @classmethod
    def _parse_data(cls, data):
        doc = Document()
        for i,block in enumerate(data.split("\f"), 1):
            # skip the empty page
            if not block.strip():
                continue
            page = Page.create(i, block)
            doc.append(page)
        return doc

    @classmethod
    def parse(cls, fp):
        if isinstance(fp, six.string_types):
            fp = open(fp)
        return cls._parse_data(fp.read())


class Page:
    def __init__(self, page, body):
        self.page = page
        self.info = Info.detect(body)
        self.body = body[self.info.start:-self.info.end]

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body):
        self._body = body

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, page):
        self._page = page

    @classmethod
    def create(cls, page, data):
        return Page(page, data)


HEADER_RE = re.compile(r'(?ms)^\nRFC (\d+)([^\n]+)\n{3}')
FOOTER_RE = re.compile(r'(?ms)\n{3}([^\n]+)\[Page (\d+)\]\n')
SPLITTER_RE = re.compile(r'\s{2,}')

class Info:
    def __init__(self, rfc, title, date, author, category, page, start, end):
        self.rfc = rfc
        self.title = title
        self.date = date
        self.author = author
        self.category = category
        self.page = page

        self.start = start
        self.end = end

    @classmethod
    def detect(self, data):
        start = 0
        end = 0
        # header section
        rfc = None
        title = None
        date = None
        m = HEADER_RE.search(data)
        if m:
            rfc = int(m.group(1))
            other = m.group(2).strip()
            if other:
                others = SPLITTER_RE.split(other)
                if len(others) == 1:
                    date = others[0]
                elif len(others) == 2:
                    title = others[0]
                    date = others[1]
            start = len(m.group(0))
        # footer section
        author = None
        category = None
        page = None
        m = FOOTER_RE.search(data)
        if m:
            other = m.group(1).strip()
            page = int(m.group(2))
            if other:
                others = SPLITTER_RE.split(other)
                if len(others) == 1:
                    author = others[0]
                elif len(others) == 2:
                    author = others[0]
                    category = others[1]
                end = len(m.group(0))
        return Info(rfc, title, date, author, category, page, start, end)
