#!/bin/sh
d="ontology-1"


for n in "01" "02" "03" "04" "05" "06" "07" "08" "09" "10" "11" "12" "13"
do
    pipenv run python ate-006-thd.py \
      --in_dataset=$d/datasets/D00000000$n.txt \
      --out_terms=$d/terms/W2D00000000$n.csv \
      --stopwords=$d/etc/stopwords.csv \
      --term_patterns=$d/etc/term_patterns.csv  \
      --min_term_length=3 --min_term_words=2 --trace=0
done

