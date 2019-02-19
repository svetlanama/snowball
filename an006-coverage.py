#!/usr/bin/env python2
#encoding: UTF-8


# networkx 2.0!!!!
import ConfigParser
import measures
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from scipy.stats import chi2_contingency

def main():

    
    # read configuration file
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini'))
    
    dataDir = config.get('main', 'dataDir')   
    dataDir = './data-pronunciation-2'





    dfn0 = pd.read_csv(dataDir + '/out-citation-network.csv', sep="\t")
    ls=[]
    for index, row in dfn0['topics'].iteritems():
        ls.append([ float(x) for x in str(row).split(";") ])
    dfn1=pd.DataFrame(data=np.array(ls))
    dfn1['entryId']=dfn0['entryId']
    dfn1.set_index('entryId', inplace=True);

    totalsFull=np.array(dfn1.sum())/dfn1.shape[0]
    #totalsFull=np.array(dfn1.sum())
    #totalsFull=totalsFull/sum(totalsFull)


    filelist=[dataDir + '/out-6500-top200-by-SPC.csv',dataDir + '/out-6500-top200-by-in_degree.csv',
              dataDir + '/out-6500-top200-by-PageRank.csv',dataDir + '/out-6500-top200-by-ECC.csv']
    #dfn2 = pd.read_csv(dataDir + '/out-6500-top200-by-SPC.csv', sep=",")
    #dfn2 = pd.read_csv(dataDir + '/out-6500-top200-by-in_degree.csv', sep=",")
    #dfn2 = pd.read_csv(dataDir + '/out-6500-top200-by-PageRank.csv', sep=",")
    #dfn2 = pd.read_csv(dataDir + '/out-6500-top200-by-ECC.csv', sep=",")
    
    for f in filelist:
        dfn2 = pd.read_csv( f , sep=",")
        dfn3=dfn2[['SPC', 'entryId']].set_index('entryId').join(dfn1, how='left').drop(['SPC'],axis=1)
        totalsReduced=np.array(dfn3.sum())/dfn3.shape[0]
        #totalsReduced=np.array(dfn3.sum())
        #totalsReduced=totalsReduced/sum(totalsReduced)
        

        chi2, p, dof, expected = chi2_contingency(np.array([totalsReduced, totalsFull]))
        print f, chi2
        
        #print {'f':f  ,'kl':measures.kl_divergence(totalsReduced, totalsFull)}
        #print {'f':f  ,'skl':measures.skl_divergence(totalsReduced, totalsFull)}
        #print {'f':f  ,'js':measures.js_divergence(totalsReduced, totalsFull)}
        #print {'f':f  ,'s2jsd':measures.s2jsd_divergence(totalsReduced, totalsFull)}
        #print {'f':f  ,'hellinger':measures.hellinger_distance(totalsReduced, totalsFull)}

    return
    
    # print totalsFull.shape, totalsReduced.shape
    plt.scatter(totalsFull, totalsReduced, alpha=0.1)
    plt.xlabel("Full Citation Network")
    plt.ylabel("Reduced Citation Network")
    plt.show()
    return
    
        
'''







'''
if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()
    print "finished"
    print "time=", t1 - t0
