#!/usr/bin/env python2
#encoding: UTF-8


# networkx 2.0!!!!
import ConfigParser
import csv
import networkx as nx
import pandas as pd
import random
import time
import numpy as np
import matplotlib.pyplot as plt

def main():

    
    # read configuration file
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini'))
    
    dataDir = config.get('main', 'dataDir')   
    
    dataDir = './data-pronunciation-3'
    n_nodes=6500
    
    n_top=100
    
    
    n_top_paths = config.getint('main', 'n_top_paths');
    
    min_in_degree = config.getint('main', 'min_in_degree');

    
    
    dfn0 = pd.read_csv(dataDir + '/out-citation-network.csv', sep="\t")
    dfn0 = dfn0.head(n_nodes)
    #print dfn0[['entryId','dist','ECC','year','url','text']].head()
    #print dfn0.columns
    #return

    dfn = dfn0[['entryId', 'referencedBy', 'referencesTo']]
    
    entries = list(dfn['entryId'])
    # print entries
    # return
    
    citation_net = nx.read_edgelist(dataDir + "/tmp-citation-network-"+str(n_nodes)+"-.edgelist", create_using=nx.DiGraph())
    # print len(citation_net.nodes())


    # network is created

    t0 = time.time()
    
    print("network is connected = ", nx.is_connected(citation_net.to_undirected()))
    
    
    # degrees of nodes
    degrees=[]
    ids=dfn0['entryId']
    for i in ids:
        k=str(i)
        try:
            x=int(citation_net.degree(k))
            degrees.append(x)
        except TypeError:
            ''' '''
    #print max(degrees)
    hst=np.histogram(degrees, bins=max(degrees)-1)
    ndm=min(len(hst[1]),len(hst[0]))
    print hst[0]
    plt.plot(np.log(hst[1][0:ndm]), np.log(hst[0][0:ndm]), 'ro')
    plt.ylabel('log(nodes)')
    plt.xlabel('log(degree)')
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
