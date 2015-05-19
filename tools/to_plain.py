#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import os

CURRENT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(CURRENT_DIR)

sys.path.append(BASE_DIR)

from rfcreader import document

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=argparse.FileType("r"))
    parser.add_argument("output", type=argparse.FileType("w"))

    args = parser.parse_args(argv[1:])

    doc = document.Document.parse(args.input)
    for page in doc.pages:
        args.output.write(page.body)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
