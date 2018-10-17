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
                    #print node_2, node_1, age
                    ages.append(age)
                    

        referencesTo=row_1.loc['referencesTo']
        if not pd.isnull(referencesTo):
            refs = referencesTo.split(';')
            for node_2 in refs:
                node_2=int(node_2)
                if node_2 in dfn.index:
                    row_2=dfn.loc[node_2]
                    age=( int(row_1.loc['year']) - int(row_2.loc['year']) )
                    citation_net.add_edge(int(node_2), int(node_1), attr_dict={'age': age  })
                    #print node_1, node_2, age
                    ages.append(age)

    #print (citation_net.edges(data=True))
    ages=np.array(ages)
    ages=ages[ages>=0]
    
    print min(ages), max(ages)
    histogram = np.histogram(ages, bins=max(ages)-min(ages))
    norm=1.0 / sum(histogram[0])
    frequencies1=histogram[0]*norm
    age_bins=histogram[1][1:]
    
    
    #print "test against Poisson distribution"
    #mu = np.argmax(frequencies1)
    #print "mu=", mu
    #print sum(frequencies1)
    #print frequencies1
    
    #mu=mu+1
    #poissondata=[stats.poisson.pmf(k,mu) for k in range(0, len(frequencies1) )]
    #poissondata=poissondata/sum(poissondata)
    #print sum(poissondata)
    #print poissondata
    
    fs=12
    plt.figure(figsize=(5,5))
    plt.ylabel('Citation Probability', fontsize=fs)
    plt.xlabel('Cited Paper Age, years', fontsize=fs) 
    plt.plot(age_bins, frequencies1, 'r', label='All Nodes')
    plt.plot(age_bins, poissondata, 'bo', label='Poisson')
    plt.legend(loc='upper right', shadow=True)
    plt.show()

    return
    
    fs=12
    #plt.figure(figsize=(5,5))
    #plt.ylabel('Citation Probability', fontsize=fs)
    #plt.xlabel('Cited Paper Age, years', fontsize=fs) 
    #plt.bar(age_bins, frequencies)
    #plt.show()
    
    
    # draw citation probability for seminal papers
    # read the selected papers
    # get the selected edges
    # get ages for a selected edges
    # draw historam of the ages
    dfn2 = pd.read_csv(dataDir + '/out-citation-network-reduced.csv', sep="\t")
    ages2=[]
    for i in dfn2.index:
        row=dfn2.loc[i]
        node_1=row.loc['Source']
        node_2=row.loc['Target']

        if node_1.isdigit():
            edges =citation_net.in_edges(nbunch=[(int(node_1))],data=True)
            for ed in edges:
                ages2.append(ed[2]['attr_dict']['age'])

        if node_2.isdigit():
            edges =citation_net.in_edges(nbunch=[(int(node_2))],data=True)
            for ed in edges:
                ages2.append(ed[2]['attr_dict']['age'])
    # print ages2
    ages2=np.array(ages2)
    ages2=ages2[ages2>=0]

    histogram2=np.histogram(ages2, bins=max(ages)-min(ages), range=(min(ages), max(ages)))
    print histogram2
    norm2=1.0 / sum(histogram2[0])
    frequencies2=histogram2[0]*norm2
    
    
    
    plt.figure(figsize=(5,5))
    plt.ylabel('Citation Probability', fontsize=fs)
    plt.xlabel('Cited Paper Age, years', fontsize=fs) 
    plt.plot(age_bins, frequencies1, 'r', label='All Nodes')
    plt.plot(age_bins, frequencies2, 'bo', label='Main Path Nodes')
    plt.legend(loc='upper right', shadow=True)
    plt.show()
    
'''







'''
if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()
    print "finished"
    print "time=", t1 - t0
