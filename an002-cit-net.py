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

def main():

    
    # read configuration file
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini'))
    
    dataDir = config.get('main', 'dataDir')   
    
    dataDir = './data-pronunciation-3'
    
    n_top=200
    
    
    n_top_paths = config.getint('main', 'n_top_paths');
    
    min_in_degree = config.getint('main', 'min_in_degree');

    
    
    
    n_nodes_list = [2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500]
    for i in xrange(0,len(n_nodes_list)):
        
        n_nodes = n_nodes_list[i]
        print "n_nodes=", n_nodes
    
    
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









        # get PageRank of nodes
        pr = nx.pagerank(citation_net, alpha=0.9)
        ids=dfn0['entryId']
        pageRanks=[]
        for i in ids:
            k=str(i)
            if k in pr:
                pageRanks.append(pr[k])
            else:
                pageRanks.append(0)
        dfn0['PageRank']=pageRanks
        # print dfn0[['entryId','PageRank']].head()






        # in-degrees of nodes
        in_degrees=[]
        ids=dfn0['entryId']
        for i in ids:
            k=str(i)
            in_degrees.append(citation_net.in_degree(k))
        dfn0['inDegree']=in_degrees










        # SPC
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
        print " n nodes=", len(s_nodes)


        # get list of all nodes
        n_minus = {}
        n_plus = {}
        for nd in citation_net.nodes():
            n_minus[nd] = -1
            n_plus[nd] = -1


        # calculate n_minus[node]
        n_minus['s'] = 1
        n_updates = 1
        while n_updates > 0:
            n_updates = 0
            for nd in n_minus:
                if n_minus[nd] < 0:
                    in_edges = [n_minus[ed] for (ed, _) in list(citation_net.in_edges([nd]))]
                    # print "in_edges=", nd, [ed for (ed, _) in list(citation_net.in_edges([nd]))]
                    if in_edges and min(in_edges) > 0:
                        # print "updated\n\n"
                        #print "in_edges=", nd, in_edges
                        n_updates += 1
                        n_minus[nd] = sum(in_edges)
            print "n_updates=", n_updates


        print  "n_minus=", n_minus
        # return

        # calculate n_plus[node]
        n_plus['t'] = 1
        n_updates = 1
        while n_updates > 0:
            n_updates = 0
            for nd in n_plus:
                if n_plus[nd] < 0:
                    out_edges = [n_plus[ed] for ( _, ed) in list(citation_net.out_edges([nd]))]
                    #print "out_edges=", nd, [ed for (ed, _) in list(citation_net.out_edges([nd]))]
                    if out_edges and  min(out_edges) > 0:
                        #print "updated\n\n"
                        n_updates += 1
                        n_plus[nd] = sum(out_edges)
            print "n_updates=", n_updates
        print  "n_plus=", n_plus
        #print list(citation_net.out_edges(['s']))

        citation_net_flow=float(n_plus['s']*n_minus['t'])
        print "citation_net_flow=", citation_net_flow



        for nd in n_plus:
            if n_plus[nd] < 0 or n_minus[nd] < 0:
                citation_net.remove_node(nd)

        print "n_nodes=", len(citation_net.nodes())
        print("network is connected = ", nx.is_connected(citation_net.to_undirected()))

        # calculate edge weights
        all_edges=citation_net.edges()
        edge_weights=[]
        for ed in all_edges:
            evg=(ed[0], ed[1], n_minus[ed[0]]*n_plus[ed[1]])
            #print evg    
            edge_weights.append( evg  )

        sorted_edge_weights=sorted(edge_weights,cmp=lambda x,y: int(np.sign(y[2]-x[2])))
        print "edge_weights=", edge_weights


        # node weights
        node_weights={}
        for nd in citation_net.nodes():
            node_weights[nd] = -1

        for evg in edge_weights:
            node_weights[evg[0]]=max(node_weights[evg[0]], evg[2] )
            node_weights[evg[1]]=max(node_weights[evg[1]], evg[2] )


        ids=dfn0['entryId']
        wgts=[]
        for i in ids:
            k=str(i)
            if k in node_weights:
                wgts.append(node_weights[k])
            else:
                wgts.append(0)
        dfn0['SPC']=wgts

        dfn0['abs_dist']=dfn0['dist'].map(abs)


        # print dfn0.head()
        dfn0.to_csv(dataDir + '/out-citation-network-extended.csv')



        print "\n\n\n============== Top by PageRank ============"
        dfn0[["entryId","abs_dist","ECC","PageRank","SPC","inDegree","year","text"]].sort_values(by=['PageRank'],ascending=False).head(n_top).to_csv(dataDir + '/out-'+str(n_nodes)+'-top'+str(n_top)+'-by-PageRank.csv')


        print "\n\n\n============== Top by ECC ============"
        dfn0[["entryId","abs_dist","ECC","PageRank","SPC","inDegree","year","text"]].sort_values(by=['ECC'],ascending=False).head(n_top).to_csv(dataDir + '/out-'+str(n_nodes)+'-top'+str(n_top)+'-by-ECC.csv')


        print "\n\n\n============== Top by SPC ============"
        dfn0[["entryId","abs_dist","ECC","PageRank","SPC","inDegree","year","text"]].sort_values(by=['SPC'],ascending=False).head(n_top).to_csv(dataDir + '/out-'+str(n_nodes)+'-top'+str(n_top)+'-by-SPC.csv')


        print "\n\n\n============== Top by abs_dist ============"
        dfn0[["entryId","abs_dist","ECC","PageRank","SPC","inDegree","year","text"]].sort_values(by=['abs_dist'],ascending=True).head(n_top).to_csv(dataDir + '/out-'+str(n_nodes)+'-top'+str(n_top)+'-by-abs_dist.csv')


        print "\n\n\n============== Top by inDegree ============"
        dfn0[["entryId","abs_dist","ECC","PageRank","SPC","inDegree","year","text"]].sort_values(by=['inDegree'],ascending=False).head(n_top).to_csv(dataDir + '/out-'+str(n_nodes)+'-top'+str(n_top)+'-by-in_degree.csv')

    return
    
    


        
'''







'''
if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()
    print "finished"
    print "time=", t1 - t0
