#!/usr/bin/env python2
#encoding: UTF-8


import pandas as pd
from nltk.stem.porter import *
from nltk.corpus import stopwords
#import libate4 as ate
#import libthd as thd

raw_datasets = (
#                ('ontology-1-baseline/terms/W2D0000000001.csv', 'ontology-1-baseline/terms-clean/W2D0000000001.csv'),
#                ('ontology-1-baseline/terms/W2D0000000002.csv', 'ontology-1-baseline/terms-clean/W2D0000000002.csv'),
#                ('ontology-1-baseline/terms/W2D0000000003.csv', 'ontology-1-baseline/terms-clean/W2D0000000003.csv'),
#                ('ontology-1-baseline/terms/W2D0000000004.csv', 'ontology-1-baseline/terms-clean/W2D0000000004.csv'),
#                ('ontology-1-baseline/terms/W2D0000000005.csv', 'ontology-1-baseline/terms-clean/W2D0000000005.csv'),

                ('ontology-1/terms/W2D0000000001.csv', 'ontology-1/terms-clean/W2D0000000001.csv'),
                ('ontology-1/terms/W2D0000000002.csv', 'ontology-1/terms-clean/W2D0000000002.csv'),
                ('ontology-1/terms/W2D0000000003.csv', 'ontology-1/terms-clean/W2D0000000003.csv'),
                ('ontology-1/terms/W2D0000000004.csv', 'ontology-1/terms-clean/W2D0000000004.csv'),
                ('ontology-1/terms/W2D0000000005.csv', 'ontology-1/terms-clean/W2D0000000005.csv'),
                ('ontology-1/terms/W2D0000000006.csv', 'ontology-1/terms-clean/W2D0000000006.csv'),
                ('ontology-1/terms/W2D0000000007.csv', 'ontology-1/terms-clean/W2D0000000007.csv'),
                ('ontology-1/terms/W2D0000000008.csv', 'ontology-1/terms-clean/W2D0000000008.csv'),
                ('ontology-1/terms/W2D0000000009.csv', 'ontology-1/terms-clean/W2D0000000009.csv'),
                ('ontology-1/terms/W2D0000000010.csv', 'ontology-1/terms-clean/W2D0000000010.csv'),
                ('ontology-1/terms/W2D0000000011.csv', 'ontology-1/terms-clean/W2D0000000011.csv'),
                ('ontology-1/terms/W2D0000000012.csv', 'ontology-1/terms-clean/W2D0000000012.csv'),
                ('ontology-1/terms/W2D0000000013.csv', 'ontology-1/terms-clean/W2D0000000013.csv')

#                ('ontology-1-baseline-acm/terms/W2D0000000001.csv', 'ontology-1-baseline-acm/terms-clean/W2D0000000001.csv'),
#                ('ontology-1-baseline-acm/terms/W2D0000000002.csv', 'ontology-1-baseline-acm/terms-clean/W2D0000000002.csv'),
#                ('ontology-1-baseline-acm/terms/W2D0000000003.csv', 'ontology-1-baseline-acm/terms-clean/W2D0000000003.csv'),
#                ('ontology-1-baseline-acm/terms/W2D0000000004.csv', 'ontology-1-baseline-acm/terms-clean/W2D0000000004.csv'),
#                ('ontology-1-baseline-acm/terms/W2D0000000005.csv', 'ontology-1-baseline-acm/terms-clean/W2D0000000005.csv'),
#                ('ontology-1-baseline-acm/terms/W2D0000000006.csv', 'ontology-1-baseline-acm/terms-clean/W2D0000000006.csv'),
#                ('ontology-1-baseline-acm/terms/W2D0000000007.csv', 'ontology-1-baseline-acm/terms-clean/W2D0000000007.csv'),
#                ('ontology-1-baseline-acm/terms/W2D0000000008.csv', 'ontology-1-baseline-acm/terms-clean/W2D0000000008.csv'),
#                ('ontology-1-baseline-acm/terms/W2D0000000009.csv', 'ontology-1-baseline-acm/terms-clean/W2D0000000009.csv'),
#                ('ontology-1-baseline-acm/terms/W2D0000000010.csv', 'ontology-1-baseline-acm/terms-clean/W2D0000000010.csv'),
#                ('ontology-1-baseline-acm/terms/W2D0000000011.csv', 'ontology-1-baseline-acm/terms-clean/W2D0000000011.csv'),
#
#    ('ontology-1-baseline-google-scholar/terms/W2D0000000001.csv', 'ontology-1-baseline-google-scholar/terms-clean/W2D0000000001.csv'),
#    ('ontology-1-baseline-google-scholar/terms/W2D0000000002.csv', 'ontology-1-baseline-google-scholar/terms-clean/W2D0000000002.csv'),
#    ('ontology-1-baseline-google-scholar/terms/W2D0000000003.csv', 'ontology-1-baseline-google-scholar/terms-clean/W2D0000000003.csv'),
#    ('ontology-1-baseline-google-scholar/terms/W2D0000000004.csv', 'ontology-1-baseline-google-scholar/terms-clean/W2D0000000004.csv'),
#    ('ontology-1-baseline-google-scholar/terms/W2D0000000005.csv', 'ontology-1-baseline-google-scholar/terms-clean/W2D0000000005.csv'),
#    ('ontology-1-baseline-google-scholar/terms/W2D0000000006.csv', 'ontology-1-baseline-google-scholar/terms-clean/W2D0000000006.csv'),
#    ('ontology-1-baseline-google-scholar/terms/W2D0000000007.csv', 'ontology-1-baseline-google-scholar/terms-clean/W2D0000000007.csv'),
#    ('ontology-1-baseline-google-scholar/terms/W2D0000000008.csv', 'ontology-1-baseline-google-scholar/terms-clean/W2D0000000008.csv'),
#    ('ontology-1-baseline-google-scholar/terms/W2D0000000009.csv', 'ontology-1-baseline-google-scholar/terms-clean/W2D0000000009.csv'),
#    ('ontology-1-baseline-google-scholar/terms/W2D0000000010.csv', 'ontology-1-baseline-google-scholar/terms-clean/W2D0000000010.csv'),
#    ('ontology-1-baseline-google-scholar/terms/W2D0000000011.csv', 'ontology-1-baseline-google-scholar/terms-clean/W2D0000000011.csv'),
#    ('ontology-1-baseline-google-scholar/terms/W2D0000000012.csv', 'ontology-1-baseline-google-scholar/terms-clean/W2D0000000012.csv'),
#
#    ('ontology-1-baseline-ms-academic/terms/W2D0000000001.csv', 'ontology-1-baseline-ms-academic/terms-clean/W2D0000000001.csv'),
#    ('ontology-1-baseline-ms-academic/terms/W2D0000000002.csv', 'ontology-1-baseline-ms-academic/terms-clean/W2D0000000002.csv'),
#    ('ontology-1-baseline-ms-academic/terms/W2D0000000003.csv', 'ontology-1-baseline-ms-academic/terms-clean/W2D0000000003.csv'),
#    ('ontology-1-baseline-ms-academic/terms/W2D0000000004.csv', 'ontology-1-baseline-ms-academic/terms-clean/W2D0000000004.csv'),
#    ('ontology-1-baseline-ms-academic/terms/W2D0000000005.csv', 'ontology-1-baseline-ms-academic/terms-clean/W2D0000000005.csv'),
#    ('ontology-1-baseline-ms-academic/terms/W2D0000000006.csv', 'ontology-1-baseline-ms-academic/terms-clean/W2D0000000006.csv'),
#    ('ontology-1-baseline-ms-academic/terms/W2D0000000007.csv', 'ontology-1-baseline-ms-academic/terms-clean/W2D0000000007.csv'),
#    ('ontology-1-baseline-ms-academic/terms/W2D0000000008.csv', 'ontology-1-baseline-ms-academic/terms-clean/W2D0000000008.csv'),
#    ('ontology-1-baseline-ms-academic/terms/W2D0000000009.csv', 'ontology-1-baseline-ms-academic/terms-clean/W2D0000000009.csv'),
#    ('ontology-1-baseline-ms-academic/terms/W2D0000000010.csv', 'ontology-1-baseline-ms-academic/terms-clean/W2D0000000010.csv'),
#    ('ontology-1-baseline-ms-academic/terms/W2D0000000011.csv', 'ontology-1-baseline-ms-academic/terms-clean/W2D0000000011.csv'),
#    ('ontology-1-baseline-ms-academic/terms/W2D0000000012.csv', 'ontology-1-baseline-ms-academic/terms-clean/W2D0000000012.csv'),
#    ('ontology-1-baseline-ms-academic/terms/W2D0000000013.csv', 'ontology-1-baseline-ms-academic/terms-clean/W2D0000000013.csv'),
#
#    ('speechsegmentation/terms/W2D0000000001.csv', 'speechsegmentation/terms-clean/W2D0000000001.csv'),
#    ('speechsegmentation/terms/W2D0000000002.csv', 'speechsegmentation/terms-clean/W2D0000000002.csv'),
#    ('speechsegmentation/terms/W2D0000000003.csv', 'speechsegmentation/terms-clean/W2D0000000003.csv'),
)

# stopwords filter
stemmer = PorterStemmer()
df_stopwords=pd.read_csv('ontology-1/out-stopwords.csv', sep="\t")
stopwords=set(df_stopwords['key'])
def does_not_contain_stopwords(s):
    #print(s)
    ws=str(s).split(' ')
    for w in ws:
        w_stemmed=stemmer.stem(w).encode('utf-8')
        if w_stemmed in stopwords:
            return False
    return True

df_prev=None
df_curr=None

for f_in, f_out in raw_datasets:

    df_terms = pd.read_csv(f_in, sep=";", header=None, names=['term', 'cvalue'])
    #print(df_terms.head())

    df_terms['nonstop'] = df_terms['term'].map(does_not_contain_stopwords)
    #print(df_terms['term'].map(does_not_contain_stopwords))
    #print(df_terms[df_terms['nonstop']].head())
    df_terms = df_terms[df_terms['nonstop']][['term', 'cvalue']].set_index('term')
    

    
    df_terms.sort_values('cvalue', ascending=False, inplace=True)
    
    df_terms[['cvalue']].to_csv(f_out, sep=";", header=None)

    

