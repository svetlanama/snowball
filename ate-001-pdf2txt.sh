#!/bin/sh

#pipenv run python  ate-001-pdf2txt.py \
#   --pdfdir=speechsegmentation/pdf \
#   --txtdir=speechsegmentation/txt_raw

#pipenv run python  ate-001-pdf2txt.py \
#   --pdfdir=ontology-1-baseline-ms-academic/pdf \
#   --txtdir=ontology-1-baseline-ms-academic/txt_raw

pipenv run python ate-001-pdf2txt.py \
   --pdfdir=ontology-1-baseline-google-scholar/pdf \
   --txtdir=ontology-1-baseline-google-scholar/txt_raw

#pipenv run python  ate-001-pdf2txt.py \
#   --pdfdir=ontology-1-baseline-acm/pdf \
#   --txtdir=ontology-1-baseline-acm/txt_raw

#pipenv run python  ate-001-pdf2txt.py \
#   --pdfdir=ontology-1-baseline/pdf \
#   --txtdir=ontology-1-baseline/txt_raw

#pipenv run python  ate-001-pdf2txt.py \
#   --pdfdir=ontology-1/pdf \
#   --txtdir=ontology-1/txt_raw
