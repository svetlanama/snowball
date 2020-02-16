#!/bin/sh

#pipenv run python ate-002-cleantxt.py \
#  --in_txt_dir=speechsegmentation/txt_raw \
#  --out_txt_dir=speechsegmentation/txt_clean

#pipenv run python ate-002-cleantxt.py \
#  --in_txt_dir=ontology-1-baseline-ms-academic/txt_raw \
#  --out_txt_dir=ontology-1-baseline-ms-academic/txt_clean

pipenv run python ate-002-cleantxt.py \
  --in_txt_dir=ontology-1-baseline-google-scholar/txt_raw \
  --out_txt_dir=ontology-1-baseline-google-scholar/txt_clean

#pipenv run python ate-002-cleantxt.py \
#  --in_txt_dir=ontology-1-baseline-acm/txt_raw \
#  --out_txt_dir=ontology-1-baseline-acm/txt_clean

#pipenv run python ate-002-cleantxt.py \
#  --in_txt_dir=ontology-1-baseline/txt_raw \
#  --out_txt_dir=ontology-1-baseline/txt_clean

#pipenv run python ate-002-cleantxt.py \
#  --in_txt_dir=ontology-1/txt_raw \
#  --out_txt_dir=ontology-1/txt_clean
