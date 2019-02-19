#!/bin/sh
PYTHONPATH=/usr/local/lib/python2.7/dist-packages  python2 r.py \
  --in_dataset=data/datasets/mnhn/auto-001.txt \
  --out_terms=data/terms/mnhn/auto-001.csv \
  --stopwords=data/etc/mnhn-stopwords.csv \
  --term_patterns=data/etc/term_patterns.csv  \
  --min_term_length=3 --min_term_words=1 --trace=0

