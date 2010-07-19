#!/usr/bin/env python
# encoding: utf-8

## WordCount reducer for Hadoop streaming example in Python
## author: Paco Nathan <ceteri@gmail.com>

import sys

word_list = {}

## collect (key,val) pairs from sort phase

for line in sys.stdin:
    try:
        word, count = line.strip().split("\t", 2)

        if word not in word_list:
            word_list[word] = int(count)
        else:
            word_list[word] += int(count)

    except ValueError, err:
        sys.stderr.write("Value ERROR: %(err)s\n%(data)s\n" % {"err": str(err), "data": line})

## emit results

for word, count in word_list.items():
    print "\t".join([word, str(count)])



