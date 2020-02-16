#!/usr/bin/env file
# -*- coding: utf-8 -*-
import pandas as pd
import libthd as thd
print("\n\n\n============\n")

files = (
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
#    ('speechsegmentation/terms/W2D0000000001.csv', 'speechsegmentation/terms-clean/W2D0000000001.csv'),
#    ('speechsegmentation/terms/W2D0000000002.csv', 'speechsegmentation/terms-clean/W2D0000000002.csv'),
#    ('speechsegmentation/terms/W2D0000000003.csv', 'speechsegmentation/terms-clean/W2D0000000003.csv'),
)
for i in range (0, len(files)-1):
	print "------starting new iteration--------"	
        df_T1 = pd.read_csv(files[i][1], sep=";", header=None, names=['term', 'cvalue']).set_index('term')
        df_T2 = pd.read_csv(files[i+1][1], sep=";", header=None, names=['term', 'cvalue']).set_index('term')
        val_eps, val_thd, val_thdr = thd.thd(df_T1, df_T2)
        print(files[i], files[i+1], 'eps',val_eps, 'thdr=', val_thdr, 'thd=', val_thd)


