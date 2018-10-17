#!/usr/bin/env python2
#encoding: UTF-8


# networkx 2.0!!!!
import ConfigParser
import csv
import networkx as nx
import pandas as pd
import random
import time

def main():

    n_nodes=5000
    
    # read configuration file
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini'))
    
    dataDir = config.get('main', 'dataDir')   
    dataDir = './data-pronunciation-2'
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
    citation_net = nx.DiGraph()
    
    for i in dfn.index:
        row = dfn.loc[i]
        node_1 = row.loc['entryId']
        if pd.notnull(row.loc['referencedBy']):
            refs = row.loc['referencedBy'].split(';')
            for ref in refs:
                node_2 = int(ref)
                if node_2 in entries:
                    #print (node_1, node_2)
                    citation_net.add_edge(node_2, node_1)
        if pd.notnull(row.loc['referencesTo']):
            refs = row.loc['referencesTo'].split(';')
            for ref in refs:
                node_2 = int(ref)
                if node_2 in entries:
                    #print (node_1, node_2)
                    citation_net.add_edge(node_1, node_2)

        # print i,node_1
    print len(citation_net.nodes())
    # nx.write_edgelist(citation_net, dataDir + "/tmp-citation-network.edgelist")


    # network is created

    t0 = time.time()
    
    
    
    
    
    print("network is connected = ", nx.is_connected(citation_net.to_undirected()))
    # remove cycles
    cycles = list(nx.simple_cycles(citation_net))
    for c in cycles:
        #print 'cycle=',c
        copies=[]
        for nd in c:
            # transform network
            # duplicate every node in the cycle
            nd2=str(nd)+'.v2'
            copies.append(nd2)
            citation_net.add_node(nd2)

        
        for nd in c:
            # transform network
            # duplicate every node in the cycle
            nd2=str(nd)+'.v2'
            #print nd2
            # print nd2
        
            # duplicate edges

            # duplicate all incoming edges
            out_edges = citation_net.in_edges(nbunch=[nd])
            for in_edge in out_edges:
                #print "in_edge", in_edge
                if str(in_edge[0])+'.v2' not in copies:
                    #print "in_edge2", in_edge
                    citation_net.add_edge(in_edge[0], nd2)


            # duplicate outcoming edges
            in_edges = citation_net.out_edges(nbunch=[nd])
            for out_edge in in_edges:
                #print "out_edge", out_edge
                if out_edge[1] not in c and str(in_edge[1])+'.v2' not in copies:
                    #print "out_edge 2", out_edge
                    citation_net.add_edge(nd2, in_edge[1])

            citation_net.add_edge(nd, nd2)
        
        # remove edges inside cycle
        for nd1 in c:
            for nd2 in c:
                if citation_net.has_edge(nd1, nd2):
                    citation_net.remove_edge(nd1, nd2)
                    citation_net.add_edge(nd1, str(nd2)+'.v2')

                if citation_net.has_edge(nd2, nd1):
                    citation_net.remove_edge(nd2, nd1)
                    citation_net.add_edge(nd2, str(nd1)+'.v2')

        #cycles2 = list(nx.simple_cycles(citation_net))
        #print cycles2
        #return
                
        # add edge from node to duplicate
        # replace outgoing edges
            
    #cycles2 = list(nx.simple_cycles(citation_net))
    #print cycles2
    print("decycled network is connected = ", nx.is_connected(citation_net.to_undirected()))
    
    # write decycled network
    nx.write_edgelist(citation_net, dataDir + "/tmp-citation-network-"+str(n_nodes)+"-.edgelist")
    return
        
'''







'''
if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()
    print "finished"
    print "time=", t1 - t0
