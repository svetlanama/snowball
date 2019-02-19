#!/usr/bin/env python2
#encoding: UTF-8
import time
import pandas as pd

autofiles=[
'data/terms/mnhn/auto-001.csv',
'data/terms/mnhn/auto-002.csv',
'data/terms/mnhn/auto-003.csv',
'data/terms/mnhn/auto-004.csv',
'data/terms/mnhn/auto-005.csv',
]
manfile='data/terms/mnhn/manual-001.csv'

mandf=pd.read_csv(manfile,sep=',')
manterms=set(mandf['term'])
for autofile in autofiles:
    autodf=pd.read_csv(autofile,sep=',')
    autoterms=set(autodf['term'])
    intersect=autoterms.intersection(manterms)
    union=autoterms.union(manterms)
    print('Jaccard measure=', len(intersect)*1.0/len(union))

