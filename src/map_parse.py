#!/usr/bin/env python
# encoding: utf-8

## mapper to parse the Enron email data, as input to MapReduce
## http://infochimps.org/datasets/enron-email-dataset--2
##
## author: Paco Nathan <ceteri@gmail.com>

import hashlib
import os
import re
import string
import sys
import urllib


def getStopWords (stopword_src):
    stopwords = set([])

    if stopword_src:
        f = open(stopword_src, "r")

        try:
            for line in f:
                line = line.strip()
                stopwords.add(line)

        except ValueError, err:
            sys.stderr.write("Value ERROR: %(err)s\n%(data)s\n" % {"err": str(err), "data": line})

        f.close()

    return stopwords


def getUUID (msg_uri):
    return hashlib.md5(msg_uri).hexdigest()


def parseRFC822 (data_dir, msg_uri):
    in_body = False
    pat = re.compile("^[\-\_]+$")
    term_count = {}
    word_bag = set([])
    date = "unknown"
    send = "unknown"
    recv = "unknown"

    try:
        path = data_dir + msg_uri

        if data_dir.startswith("http:"):
            f = urllib.urlopen(path)
        else:
            f = open(path, "r")

        for line in f:
            line = line.strip()

            if in_body:
                l = re.sub("[^a-z0-9\-\_]", " ", line.lower()).split(" ")
                #print l

                for word in l:
                    if not re.search(pat, word) and (len(word) > 0):
                        # term counts within a doc

                        if word not in term_count:
                            term_count[word] = 1
                        else:
                            term_count[word] += 1

			# "bag of word" (unique terms)
                        word_bag.add(word)

            elif len(line) < 1:
                # RFC822 first blank line terminates header section in email message
                in_body = True

            elif line.startswith("Date:"):
                # email date
                date = line.strip("Date: ")

            elif line.startswith("From:"):
                # email sender
                send = line.split(" ")[1]

            elif line.startswith("To:"):
                # email recipient
                recv = line.split(" ")[1].strip(",")

        f.close()

    except ValueError, err:
        sys.stderr.write("Value ERROR: %(err)s\n%(data)s\n" % {"err": str(err), "data": str(l)})

    return term_count, word_bag, date, send, recv


def getTermList (word_bag):
    # construct a list of unique words, sorted in alpha order

    term_list = list(map(lambda x: x, word_bag))
    term_list.sort()

    return term_list


def getTermFreq (term_count, term_list):
    # calculate term frequencies

    sum_tf = float(sum(term_count.values()))
    term_freq = {}

    for i in range(0, len(term_list)):
        word = term_list[i]
        term_freq[word] = float(term_count[word]) / sum_tf

    return term_freq


def emit (msg_uri, doc_id, date, send, recv, term_list, term_freq, stopwords):
    # emit document (email message) metadata
    print "\t".join([doc_id, "d", msg_uri, date])

    # emit sender/receiver social graph
    print "\t".join([send, "s", recv, doc_id])

    # emit co-occurring terms, with pairs in canonical order
    # (lower triangle of the cross-product)

    for i in range(0, len(term_list)):
        term = term_list[i]

        if not term in stopwords:
            print "\t".join([term, "f", "%.5f" % term_freq[term], doc_id])

            for j in range(0, len(term_list)):
                if i != j:
                    co_term = term_list[j]

                    if not co_term in stopwords:
                        print "\t".join([term, "c", co_term, doc_id])


def main (data_dir, stopword_src):
    # set up the stopword list
    stopwords = getStopWords(stopword_src)

    # scan input for list of documents to parse

    for line in sys.stdin:
        msg_uri = line.strip()

        try:
            doc_id = getUUID(msg_uri)
            term_count, word_bag, date, send, recv = parseRFC822(data_dir, msg_uri)
            term_list = getTermList(word_bag)
            term_freq = getTermFreq(term_count, term_list)
            emit(msg_uri, doc_id, date, send, recv, term_list, term_freq, stopwords)

        except ValueError, err:
            sys.stderr.write("Value ERROR: %(err)s\n%(data)s\n" % {"err": str(err), "data": msg_uri})


if __name__ == "__main__":
    data_dir = sys.argv[1]
    stopword_src = None

    if len(sys.argv) > 2:
        stopword_src = sys.argv[2]

    main(data_dir, stopword_src)
