#!/usr/bin/env python2
#encoding: UTF-8

import ConfigParser
import csv
import networkx as nx
import pandas as pd
import numpy as np
import random
import time
import matplotlib.pyplot as plt
import scipy.stats as stats

def main():
    ''
    # read configuration file
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini'))
    
    dataDir = config.get('main', 'dataDir')    
    n_top_paths = config.getint('main', 'n_top_paths');

    
    
    dfn0 = pd.read_csv(dataDir + '/out-citation-network.csv', sep="\t")
    #print dfn0[['entryId','dist','year','url','text']].head()
    
    dfn = dfn0.set_index(['entryId'])
    # print dfn.head()
    # print dfn.index
    # print dfn.loc[dfn.index[0]]
    # return

    dfn = dfn[['year', 'referencedBy', 'referencesTo']].drop_duplicates()
    #print dfn.head()
    #return
    #print type(dfn.index[0])
    #return
    #entries = list(dfn.index)
    #print type(entries[0])
    #print dfn['entryId']
    #return
    
    citation_net = nx.DiGraph()
    
    ages=[]
    
    for node_1 in dfn.index:
        row_1 = dfn.loc[node_1]
        
        # print row_1.loc['referencedBy']
        referencedBy=row_1.loc['referencedBy']
        if not pd.isnull(referencedBy):
            refs = referencedBy.split(';')
            for node_2 in refs:
                node_2=int(node_2)
                if node_2 in dfn.index:
                    #print (node_1, node_2)
                    row_2=dfn.loc[node_2]
                    age=( int(row_2.loc['year']) - int(row_1.loc['year']) )
                    citation_net.add_edge(int(node_2), int(node_1), attr_dict={'age': age  })
                    # print node_2, node_1, age
                    # ages.append(age)
                    

        referencesTo=row_1.loc['referencesTo']
        if not pd.isnull(referencesTo):
            refs = referencesTo.split(';')
            for node_2 in refs:
                node_2=int(node_2)
                if node_2 in dfn.index:
                    row_2=dfn.loc[node_2]
                    age=( int(row_1.loc['year']) - int(row_2.loc['year']) )
                    citation_net.add_edge(int(node_2), int(node_1), attr_dict={'age': age  })
                    # print node_1, node_2, age
                    # ages.append(age)

    # print (citation_net.nodes(data=False))
    
    degrees=dict(citation_net.in_degree())
    degrees=degrees.values()
    print (degrees)
    print min(degrees), max(degrees)
    histogram = np.histogram(degrees, bins=max(degrees)-min(degrees))
    #norm=1.0 / sum(histogram[0])
    #frequencies1=np.log(histogram[0]*norm)
    frequencies1=np.log(histogram[0])
    degree_bins=np.log(histogram[1][1:])
    
    
    fs=12
    plt.figure(figsize=(12,9))
    plt.ylabel('Log(Number of papers)', fontsize=fs)
    plt.xlabel('Log(Number of references)', fontsize=fs) 
    plt.plot(degree_bins, frequencies1, 'r')
    # plt.plot(degree_bins, poissondata, 'bo', label='Poisson')
    plt.legend(loc='upper right', shadow=True)
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
