#!/bin/bash -x

## run analytics on the Enron email data set:
##   keyword extraction
##   co-occurrence analysis
##   TF-IDF to filter terms
##   sender/receiver social graph

DATA_DIR=/Users/paco/src/ceteri-mapred/
#DATA_DIR=http://ceteri-mapred.s3.amazonaws.com/

DATA_LST=msgs.tsv

## override to limit processing to a subset, for testing...
#N_DOCS=`wc -l < $DATA_LST`
N_DOCS=20

head -$N_DOCS $DATA_LST \
 | src/map_parse.py $DATA_DIR stopwords > dat.parsed
## tuple: doc_id, "d", msg_uri, date
## tuple: send, "s", recv, doc_id
## tuple: term, "f", tf, doc_id
## tuple: term, "c", co_term, doc_id

cat dat.parsed | sort | src/red_idf.py $N_DOCS > dat.idf
## tuple: doc_id, "d", msg_uri, date
## tuple: send, "s", recv, doc_id
## tuple: term, "i", idf, count
## tuple: term, "p", co_term, prob_cooc
## tuple: term, "t", tfidf, doc_id
## tuple: term, "m", max_tfidf

cat dat.idf | src/util_extract.py m > thresh.tsv
## select only the "m" tuples, then run stats 
## analysis in R to choose a TFIDF threshold

T_THRESH=0.0633

cat dat.idf | src/map_filter.py | sort | src/red_filter.py $T_THRESH > dat.filter
## similar results as "red_idf.py" except that co-occurrence 
## pairs have had a high-pass filter applied


## convert the sender/receiver social graph into CSV format
## for Gephi visualization

cat dat.parsed | src/util_extract.py s | src/util_gephi.py | sort -u > graph.csv
