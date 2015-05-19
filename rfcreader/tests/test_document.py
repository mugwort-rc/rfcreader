# -*- coding: utf-8 -*-

import os.path

from .. import document

CURRENT_PATH = os.path.dirname(__file__)
MODULE_PATH = os.path.dirname(CURRENT_PATH)
BASE_PATH = os.path.dirname(MODULE_PATH)
RFC1_PATH = os.path.join(BASE_PATH, "test_data/rfc1.txt")

def gen_blocks():
    text = open(RFC1_PATH).read()
    return text.split("\f")


def test_document():
    doc = document.Document.parse(RFC1_PATH)
    assert len(doc.pages) == 11

def test_page():
    blocks = gen_blocks()

    block1 = blocks[0]
    page1 = document.Page.create(1, block1)
    assert page1.info.page == 1

    no_except = True
    try:
        index = block1.index(page1.body)
    except IndexError:
        no_except = False
        index = -1
    assert no_except == True
    assert index == 0
    assert index != -1

    block2 = blocks[1]
    page2 = document.Page.create(2, block2)
    assert page2.info.page == 2

    no_except = True
    try:
        index = block2.index(page2.body)
    except IndexError:
        no_except = False
        index = -1
    assert no_except == True
    assert index != 0
    assert index != -1


def test_info():
    blocks = gen_blocks()

    info1 = document.Info.detect(blocks[0])
    assert info1.author == "Crocker"
    assert info1.category is None
    assert info1.page == 1

    info2 = document.Info.detect(blocks[1])
    assert info2.rfc == 1
    assert info2.title == "Host Software"
    assert info2.date == "7 April 1969"
    assert info2.author == "Crocker"
    assert info2.category is None
    assert info2.page == 2
