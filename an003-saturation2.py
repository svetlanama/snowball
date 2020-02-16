#!/usr/bin/env python2
#encoding: UTF-8


# networkx 2.0!!!!
import ConfigParser
import csv
import networkx as nx
import numpy as np
import pandas as pd
import random
import time
import scipy.stats
import matplotlib.pyplot as plt


def jaccard_similarity(list1, list2):
    intersection = float(len(list(set(list1).intersection(list2))))
    #print(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection / union)

def main():

    
    # read configuration file
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini'))
    # n_top_paths = config.getint('main', 'n_top_paths');
    # min_in_degree = config.getint('main', 'min_in_degree');
    #dataDir = config.get('main', 'dataDir')   
    
    dataDir = './data-pronunciation-3'
    n_top = 200
    
    n_top_subset=60

    print "by-SPC", n_top_subset
    print "i, n_nodes, pearsonR[0], jsim"
    n_nodes_list = [2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500]
    iMax=len(n_nodes_list)
    for i in xrange(1,iMax):
        
        n_nodes = n_nodes_list[i-1]
        topNFile = dataDir + '/out-' + str(n_nodes) + '-top' + str(n_top) + '-by-SPC.csv'
        # topNFile = dataDir + '/out-'+str(n_nodes)+'-top'+str(n_top)+'-by-in_degree.csv'
        dfn0 = pd.read_csv(topNFile).head(n_top_subset)
        ranked1=list(dfn0['entryId'])
        # print ranked1

        n_nodes = n_nodes_list[i]
        topNFile = dataDir + '/out-' + str(n_nodes) + '-top' + str(n_top) + '-by-SPC.csv'
        # topNFile = dataDir + '/out-'+str(n_nodes)+'-top'+str(n_top)+'-by-in_degree.csv'
        dfn0 = pd.read_csv(topNFile).head(n_top_subset)
        ranked2=list(dfn0['entryId'])
        # print ranked2
  
        pairs={}
        for uid in ranked1:
            if uid not in pairs:
                pairs[uid]=[n_top_subset, n_top_subset]
            pairs[uid][0]=ranked1.index(uid)
        for uid in ranked2:
            if uid not in pairs:
                pairs[uid]=[n_top_subset, n_top_subset]
            pairs[uid][1]=ranked2.index(uid)
        pairs=np.transpose(np.array(pairs.values()))
        # print pairs

        #plt.plot(pairs[0], pairs[1], 'ro')
        #plt.ylabel('log(nodes)')
        #plt.xlabel('log(degree)')
        #plt.show()
        pearsonR=scipy.stats.pearsonr(pairs[0], pairs[1])
        
        
        jsim=jaccard_similarity(ranked1, ranked2)
        
        print i, n_nodes, pearsonR[0], jsim
        # return
    
    return
    
    

        
'''







'''
if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()
    print "finished"
    print "time=", t1 - t0
