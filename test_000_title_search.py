#!/usr/bin/env python2
#encoding: UTF-8
import pandas as pd
import time
import ConfigParser
import academicdownload as ad
import json
import re
import random

import sys
reload(sys)
sys.path.insert(0, '..')
sys.setdefaultencoding('utf8')

'''



'''
clearer=re.compile(r'\W+')
def get_expression(txt):
    s=str(txt).lower()
    s=clearer.sub(' ',s)
    return "Ti='"+s+"'"
'''



'''
def search_by_title(title, api, verbose):
    response = api.callApi(get_expression(title), 'Id,Ti,Y,RId,F.FN,F.FN,F.FId,AA.AuId,AA.AuN,AA.AfN,AA.AfId,E,ECC', verbose)
    if len(response)>0:
        pub=response[0]
        return pub.toList()
    else:
        return [None] * len(ad.Entry.columns())
'''



'''
def main():
    
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini'))
    
    restEndpoint=json.loads(config.get('main', 'restEndpoint'))
  
    subscriptionKey = config.get('main', 'subscriptionKey');
    api = ad.Api(subscriptionKey, restEndpoint)
    verbose=False

    # title='A comparison of eleven static heuristics for mapping a class of independent tasks onto heterogeneous distributed computing systems'
    #
    # print(search_by_title(title, api, verbose))
    # return

    refs=pd.read_csv('data-minuhin/refs-000.csv', sep='\t')
    found_refs=refs[['title']].apply(lambda x: search_by_title(x['title'], api, verbose), axis=1, result_type='expand')
    found_refs.columns=ad.Entry.columns()
    found_refs['ref']=refs['ref']
    #found_refs=refs[['title']].apply(lambda x: random.choice([[None,None,None], [1,2,3]]), axis=1, result_type='expand').dropna()

    found_refs.to_csv('data-minuhin/refs-000-extended.csv')



if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()
    print "finished"
    print "time=", t1 - t0
