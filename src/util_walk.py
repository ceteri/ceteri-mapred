#!/usr/bin/env python
# encoding: utf-8

## walk a directory tree, emitting all file names
## usage: ./util_walk.py <path>
##
## author: Paco Nathan <ceteri@gmail.com>

import os
import sys

def walk (path):
    for root, dirs, files in os.walk(path):
        for name in files:
            abs_path = os.path.join(root, name)
            print abs_path


def main (path):
    walk(path)


if __name__ == "__main__":
    path = sys.argv[1]
    main(path)
