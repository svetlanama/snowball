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

def p2():

    # different similarity measures
    nNodes=[3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500]
    
    #Spearman correlation + KL-divergence, N=60
    sc_60=[0.973869466428722, 0.624504707959419,  0.990897590585305,  0.998212842152432,  0.971009858747657,  0.999470528629491,  0.999265318396617,  0.999206388547784]
    
    #Spearman correlation + KL-divergence, N=100
    sc_100=[0.962612940230374, 0.679552264537793,  0.995367663390342,  0.998998246921014,  0.968314110882006,  0.999774464035644,  0.989745919307126,  0.999793383516234]

    #Spearman correlation + KL-divergence, N=140
    sc_140 = [0.967518174561452, 0.745560470483132,  0.993947250783483,  0.993988783647997,  0.964321809925807,  0.99986426607338,  0.973316207963689,  0.994930582244779]
    
    #Spearman correlation + KL-divergence, N=180
    sc_180 = [0.97046171301994, 0.820458261039812, 0.979411557094422 ,  0.988427050430486,  0.967983851195204,  0.999920934236045,  0.966215652835786,  0.992659065641679]
    
    
    plt.plot(nNodes, sc_60, 'go', nNodes, sc_100, 'rv', nNodes, sc_140, 'bx', nNodes, sc_180, 'bs', linestyle='solid')
    plt.ylim((0, 1.1))
    # plt.plot(np.log(hst[1][0:ndm]), np.log(hst[0][0:ndm]), 'ro')
    plt.ylabel('Spearman Rank Correlation')
    plt.xlabel('Citation Network Size, M')
    plt.show()

def p1():

    # different similarity measures
    nNodes=[3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500]
    
    #Spearman correlation + KL-divergence, N=100
    sc_kl=[0.9626, 0.6796, 0.9954, 0.9990, 0.9683, 0.9998, 0.9897, 0.9998]
    
    # Spearman correlation + Symmetric KL-divergence - good, N=100
    sc_skl=[-0.485891714869178, 0.578509097781629, 0.480639622466594, 0.998928302073005, 0.287849392790962, 0.69147903769069, 0.953334831051987, 0.949416619424925]

    # Spearman correlation + Jensen–Shannon divergence - average, N=100
    sc_js = [0.737957324335054, 0.418419888922229, 0.694291583301245, 0.742904245265443, 0.986762676267627, 0.615635759866559, 0.997871509124007, 0.787263685197431]
    
    plt.plot(nNodes, sc_kl, 'go', nNodes, sc_skl, 'rv', nNodes, sc_js, 'bx', linestyle='solid')
    plt.ylim((0, 1.1))
    # plt.plot(np.log(hst[1][0:ndm]), np.log(hst[0][0:ndm]), 'ro')
    plt.ylabel('Spearman Rank Correlation')
    plt.xlabel('Citation Network Size, M')
    plt.show()
    return
    

        
'''







'''
if __name__ == "__main__":
    t0 = time.time()
    # p1()
    p2()
    t1 = time.time()
    print "finished"
    print "time=", t1 - t0
