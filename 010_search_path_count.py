#!/usr/bin/env python2
#encoding: UTF-8


# networkx 2.0!!!!
import networkx as nx
import time
import pandas as pd
import ConfigParser
import csv

def main():

    
    # read configuration file
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini'))
    
    dataDir = config.get('main', 'dataDir')    
    n_top_paths = config.getint('main', 'n_top_paths');

    
    
    dfn0 = pd.read_csv(dataDir + '/out-citation-network.csv',sep="\t")
    #print dfn0[['entryId','dist','year','url','text']].head()

    dfn=dfn0[['entryId','referencedBy','referencesTo']]
    
    entries=list(dfn['entryId'])
    #print type(entries[0])
    
    citation_net=nx.DiGraph()
    
    for i in dfn.index:
        row=dfn.loc[i]
        node_1=row.loc['entryId']
        if pd.notnull(row.loc['referencedBy']):
            refs=row.loc['referencedBy'].split(';')
            for ref in refs:
                node_2=int(ref)
                if node_2 in entries:
                    #print (node_1, node_2)
                    citation_net.add_edge(node_2, node_1)
        if pd.notnull(row.loc['referencesTo']):
            refs=row.loc['referencesTo'].split(';')
            for ref in refs:
                node_2=int(ref)
                if node_2 in entries:
                    #print (node_1, node_2)
                    citation_net.add_edge(node_1, node_2)

        # print i,node_1
    print len(citation_net.nodes())
    nx.write_edgelist(citation_net, dataDir + "/tmp-citation-network.edgelist")

    t0 = time.time()
    
    # get nodes having zero in_degree and connect them to source node (id=s)
    s_nodes = citation_net.in_degree()
    for nd in list(s_nodes):
        if nd[1] == 0:
            citation_net.add_edge('s', nd[0])

    # gen nodes having zero out_degree and connect them to target node (id=t)
    t_nodes = citation_net.out_degree()
    for nd in list(t_nodes):
        if nd[1] == 0:
            citation_net.add_edge(nd[0], 't')
    
    print "1 source and target added", (time.time()-t0)
    print("network is connected = ", nx.is_connected(citation_net.to_undirected()))
    paths = list(nx.all_simple_paths(citation_net, source='s', target='t'))
    print "2 paths calculated", (time.time() -t0)
    print "   n_paths=", len(paths)

    print "edge weights - start"
    dct = {}
    for p in paths:
        for iN in xrange(1, len(p)):
            k = (p[iN-1], p[iN])
            if k in dct:
                dct[k] += 1
            else:
                dct[k] = 1
    #print dct
    print "3 edge weights done" , (time.time()-t0)

    nx.set_edge_attributes(citation_net, dct, 'spc')
    nx.write_edgelist(citation_net, dataDir + '/tmp-citation-network-spc.edgelist')

    # assign weight to each path
    print "4 assign weight to each path", (time.time()-t0)
    weighted_paths = []
    for path in paths:
        path_resistance = 0
        for iN in xrange(1, len(path)):
            k = (path[iN-1], path[iN])
            path_resistance += 1.0 / dct[k]
        item = (path_resistance, path)
        #print item
        weighted_paths.append(item)

    print "5 path weights - done", (time.time()-t0)
    
    sorted_weighted_paths = sorted(weighted_paths, key=lambda x: x[0])
    #print 'sorted_weighted_paths=', sorted_weighted_paths[:n_top_paths]
    print "6 sorted_weighted_paths - done", (time.time()-t0)

    # get main paths
    # show paths having minimal resistance
    path_resistance_threshold=sorted_weighted_paths[n_top_paths][0]
    selected_paths = [x for x in sorted_weighted_paths if x[0]<=path_resistance_threshold]
    
    # compose network in the selected paths
    reduced_citation_net = nx.DiGraph()
    for p in selected_paths:
        path = p[1]
        for i in xrange(1, len(path)):
            reduced_citation_net.add_edge(path[i-1], path[i], attr_dict={'spc':dct[(path[i-1], path[i])]})
    
    reduced_nodes = reduced_citation_net.nodes()
    for nd1 in reduced_nodes:
        for nd2 in reduced_nodes:
            if (nd1, nd2) in dct:
                reduced_citation_net.add_edge(nd1, nd2, attr_dict={'spc':dct[(nd1, nd2)]})
    
    nx.write_edgelist(reduced_citation_net, dataDir + '/tmp-citation-network-reduced.edgelist')
    
    print reduced_citation_net.nodes()

    node_ids=[]
    for x in reduced_citation_net.nodes():
        try:
            n=int(x)
            node_ids.append(n)
        except ValueError:
            "NaN"
    selected_nodes=pd.DataFrame(pd.Series(node_ids),columns=['entryId'])
    #print selected_nodes
    
    snds=pd.merge(dfn0[['entryId','dist','year','url','text']], selected_nodes, how='inner', left_on='entryId', right_on='entryId' )
    print snds

    snds.to_csv(dataDir + '/out-citation-network-reading-plan.csv', sep="\t", quoting=csv.QUOTE_NONNUMERIC, )
    
    print "Output is written to " + dataDir + '/out-citation-network-reading-plan.csv'
    
    return   
'''







'''
if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()
    print "finished"
    print "time=", t1 - t0
