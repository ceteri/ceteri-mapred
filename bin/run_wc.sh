#!/bin/bash -x

## a very simple "WordCount" app

cat README | src/map_wc.py | sort | src/red_wc.py | sort -k2 -nr > dat.wc
## tuple: word, count
