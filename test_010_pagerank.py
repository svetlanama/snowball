#!/usr/bin/env python2
#encoding: UTF-8

# select nodes using PageRank score
# appropriate for introductory reading plan

# networkx 2.0!!!!
import ConfigParser
import csv
import networkx as nx
import pandas as pd
import random
import time

def main():

    
    # read configuration file
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini'))
    
    dataDir = config.get('main', 'dataDir')   
    #dataDir = './data'
    n_top_paths = config.getint('main', 'n_top_paths');
    
    max_citation_net_nodes = config.getint('main', 'max_citation_net_nodes');

    
    
    dfn0 = pd.read_csv(dataDir + '/out-citation-network.csv', sep="\t")
    #print dfn0[['entryId','dist','year','url','text']].head()

    dfn = dfn0[['entryId', 'referencedBy', 'referencesTo']].head(max_citation_net_nodes)
    
    entries = list(dfn['entryId'])
    #print type(entries[0])
    
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
    nx.write_edgelist(citation_net, dataDir + "/tmp-citation-network.edgelist")

    t0 = time.time()
    
    
    
    
    
    print("network is connected = ", nx.is_connected(citation_net.to_undirected()))
    
    # remove cycles
    n_cycles = 0
    try:
        ccl = nx.find_cycle(citation_net, orientation='original')
        n_cycles = n_cycles + 1
    except:
        ccl = False
    while ccl:
        c=set()
        for p in ccl:
            c.add(p[0])
            c.add(p[1])
        print 'cycle #',n_cycles, "time=", time.time() - t0
        print c

        copies = []
        for nd in c:
            # transform network
            # duplicate every node in the cycle
            nd2 = str(nd) + '.v2'
            copies.append(nd2)
            citation_net.add_node(nd2)

        
        for nd in c:
            # transform network
            # duplicate every node in the cycle
            nd2 = str(nd) + '.v2'
            #print nd2
            # print nd2
        
            # duplicate edges

            # duplicate all incoming edges
            out_edges = citation_net.in_edges(nbunch=[nd])
            for in_edge in out_edges:
                #print "in_edge", in_edge
                if str(in_edge[0]) + '.v2' not in copies:
                    #print "in_edge2", in_edge
                    citation_net.add_edge(in_edge[0], nd2)


            # duplicate outcoming edges
            in_edges = citation_net.out_edges(nbunch=[nd])
            for out_edge in in_edges:
                #print "out_edge", out_edge
                if out_edge[1] not in c and str(in_edge[1]) + '.v2' not in copies:
                    #print "out_edge 2", out_edge
                    citation_net.add_edge(nd2, in_edge[1])

            citation_net.add_edge(nd, nd2)
        
        # remove edges inside cycle
        for nd1 in c:
            for nd2 in c:
                if citation_net.has_edge(nd1, nd2):
                    citation_net.remove_edge(nd1, nd2)
                    citation_net.add_edge(nd1, str(nd2) + '.v2')

                if citation_net.has_edge(nd2, nd1):
                    citation_net.remove_edge(nd2, nd1)
                    citation_net.add_edge(nd2, str(nd1) + '.v2')

        #cycles2 = list(nx.simple_cycles(citation_net))
        #print cycles2
        #return
                
        # add edge from node to duplicate
        # replace outgoing edges
        try:
            ccl = nx.find_cycle(citation_net, orientation='original')
            n_cycles = n_cycles + 1
        except:
            ccl = False
   

    #cycles2 = list(nx.simple_cycles(citation_net))
    #print cycles2
    print("decycled network is connected = ", nx.is_connected(citation_net.to_undirected()))
    #return
    
    s_nodes = list(citation_net.nodes())
    for nd in list(s_nodes):
        # print "node ", nd
        # get nodes having zero in_degree and connect them to source node (id=s)
        if len(citation_net.in_edges(nbunch=[nd])) == 0:
            # print "add edge s->", nd
            citation_net.add_edge('s', nd)
            
        # get nodes having zero out_degree and connect them to target node (id=t)
        if len(citation_net.out_edges(nbunch=[nd])) == 0:
            # print "add edge ", nd, "->t"
            citation_net.add_edge(nd, 't')
    # return

    print "1 source and target added", (time.time()-t0)
    print("network is connected = ", nx.is_connected(citation_net.to_undirected()))
    
    cycles = list(nx.simple_cycles(citation_net))
    print " number of cycles=", len(cycles)
    #return
    
    # calculate PageRank values
    print "calculate PageRank values ..."

    node_ids = nx.pagerank(citation_net)

    print "done"
    
    # select the most valuable nodes
    sorted_node_weights = sorted(node_ids.values() )
    wmin = sorted_node_weights[n_top_paths]
    for nid in node_ids.keys():
        if node_ids[nid]<wmin:
            del node_ids[nid]

    print "wmin=", wmin, " len(node_ids)=", len(node_ids), node_ids
    
    max_weight = float(max(node_ids.values()))

    for nd in node_ids:
        node_ids[nd] = node_ids[nd] / max_weight

    selected_nodes = pd.DataFrame([(nd, node_ids[nd]) for nd in node_ids], columns=['entryId', 'entryWeight'])
    selected_nodes['entryId'] = selected_nodes['entryId'].map(lambda x: int(str(x)) if str(x).isdigit() else None )

    snds = pd.merge(dfn0[['entryId', 'dist', 'year', 'url', 'text']], selected_nodes, how='inner', left_on='entryId', right_on='entryId')
    print snds

    fname=dataDir + '/out-citation-network-reading-plan-'+str(n_top_paths)+'-of-'+str(max_citation_net_nodes)+'-by-pagerank.csv'
    snds.to_csv(fname, sep="\t", quoting=csv.QUOTE_NONNUMERIC)
    
    print "Output is written to " + fname
    
    ## create reduced network for visualisation
    # reduced_citation_net = nx.DiGraph()
    # for ed in selected_edges:
    #    reduced_citation_net.add_edge(ed[0], ed[1], weight=ed[2])
    
    # nx.write_weighted_edgelist(reduced_citation_net, dataDir + "/out-citation-network-reduced.edgelist")
    
    # print "Reduced network is written to " + dataDir + '/out-citation-network-reduced.edgelist'
    return


        
'''







'''
if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()
    print "finished"
    print "time=", t1 - t0
