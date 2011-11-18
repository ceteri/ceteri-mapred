#!/bin/bash -x

export JAVA_HOME=/Library/Java/Home
export HADOOP_INSTALL=~/src/hadoop-0.20.1
export HADOOP=$HADOOP_INSTALL/bin/hadoop

$HADOOP dfs -mkdir txt
$HADOOP dfs -put README txt/

$HADOOP jar $HADOOP_INSTALL/contrib/streaming/hadoop-0.20.1-streaming.jar \
  -mapper  ./src/map_wc.py \
  -reducer  ./src/red_wc.py \
  -input   txt/* \
  -output  foo

$HADOOP dfs -ls foo/*
$HADOOP dfs -cat foo/*
