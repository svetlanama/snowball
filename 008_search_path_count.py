#!/usr/bin/env python2
#encoding: UTF-8

# select nodes using PageRank score
# appropriate for latest publication reading
# and historical perspective

# networkx 2.0!!!!
import ConfigParser
import csv
import networkx as nx
import pandas as pd
import random
import time


def remove_cycles(citation_net):
    t0 = time.time()
    # remove cycles
    n_cycles = 0
    ccl = True
    while ccl:
        try:
            ccl = nx.find_cycle(citation_net, orientation='original')
            n_cycles = n_cycles + 1
        except:
            ccl = False
            break

        cycle = set()
        for p in ccl:
            cycle.add(p[0])
            cycle.add(p[1])
        print 'cycle #', n_cycles, "time=", time.time() - t0
        print cycle
        cycle = list(cycle)

        # remove edges inside cycle
        if len(cycle) == 1:
            citation_net.remove_edge(cycle[0], cycle[0])
            continue

        # transform
        for nd in cycle:
            # create preprint
            nd2 = str(nd) + '.v2'
            citation_net.add_node(nd2)

            # move out edges for nd
            out_edges = citation_net.out_edges(nbunch=[nd])
            for out_edge in out_edges:
                # print "out_edge", out_edge
                target = out_edge[1]
                if target in cycle:
                    # edge is inside cycle
                    # remove edge inside cycle
                    citation_net.remove_edge(nd, target)

                    # add edge to preprint
                    citation_net.add_edge(nd, str(target)+'.v2')
                else:
                    # edge is outsite cycle
                    # move outgoing edge to preprint
                    citation_net.remove_edge(nd, target)
                    citation_net.add_edge(nd2, target)
            # connect paper to its preprint
            citation_net.add_edge(nd, nd2)

# import matplotlib.pyplot as plt
# citation_net = nx.DiGraph()
# node_1="n1"
# node_2="n2"
# node_3="n3"
# node_4="n4"

# citation_net.add_edge(node_1, node_2)
# citation_net.add_edge(node_2, node_3)
# citation_net.add_edge(node_3, node_1)

# citation_net.add_edge(node_1, node_2)
# citation_net.add_edge(node_2, node_1)
# citation_net.add_edge(node_3, node_1)
# citation_net.add_edge(node_2, node_4)

# citation_net.add_edge(node_1, node_2)
# citation_net.add_edge(node_2, node_1)
# citation_net.add_edge(node_3, node_1)
# citation_net.add_edge(node_3, node_2)
# citation_net.add_edge(node_2, node_4)
# citation_net.add_edge(node_1, node_4)
#
# nx.draw(citation_net, with_labels=True, pos=nx.spring_layout(citation_net))
# plt.draw()
# plt.show()
# #
# remove_cycles(citation_net)
# nx.draw(citation_net, with_labels=True, pos=nx.spring_layout(citation_net))
# plt.draw()
# plt.show()
# exit()


def spc(citation_net):

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
                    # print "in_edges=", nd, in_edges
                    n_updates += 1
                    n_minus[nd] = sum(in_edges)
        print "n_updates=", n_updates

    # print  "n_minus=", n_minus
    # return

    # calculate n_plus[node]
    n_plus['t'] = 1
    n_updates = 1
    while n_updates > 0:
        n_updates = 0
        for nd in n_plus:
            if n_plus[nd] < 0:
                out_edges = [n_plus[ed] for (_, ed) in list(citation_net.out_edges([nd]))]
                # print "out_edges=", nd, [ed for (ed, _) in list(citation_net.out_edges([nd]))]
                if out_edges and min(out_edges) > 0:
                    # print "updated\n\n"
                    n_updates += 1
                    n_plus[nd] = sum(out_edges)
        print "n_updates=", n_updates
    # print  "n_plus=", n_plus
    # print list(citation_net.out_edges(['s']))

    citation_net_flow = float(n_plus['s'] * n_minus['t'])
    print "citation_net_flow=", citation_net_flow

    for nd in n_plus:
        if n_plus[nd] < 0 or n_minus[nd] < 0:
            citation_net.remove_node(nd)

    # print "n_nodes=", len(citation_net.nodes())
    # print "edges=", citation_net.edges()
    print("network is connected = ", nx.is_connected(citation_net.to_undirected()))

    # calculate edge weights
    all_edges = citation_net.edges()
    edge_weights = []
    for ed in all_edges:
        evg = (ed[0], ed[1], n_minus[ed[0]] * n_plus[ed[1]])
        # print evg
        edge_weights.append(evg)

    # sorted_edge_weights = sorted(edge_weights, cmp=lambda x, y: (1 if y[2]>x[2] else -1) )
    # print edge_weights

    # wmin = sorted_edge_weights[n_top_paths][2]
    # selected_edges = [ed for ed in sorted_edge_weights if ed[2] >= wmin]
    # print "wmin=", wmin  # , " len(selected_edges)=", len(selected_edges) #, selected_edges

    node_weighs = {}
    #    for ed in edge_weights:
    #        if ed[0] not in node_ids:
    #            node_ids[ed[0]] = 0
    #
    #        if node_ids[ed[0]] < ed[2]:
    #            node_ids[ed[0]] = ed[2]
    #
    #        if ed[1] not in node_ids:
    #            node_ids[ed[1]] = 0
    #
    #        if node_ids[ed[1]] < ed[2]:
    #            node_ids[ed[1]] = ed[2]

    for ed in edge_weights:
        if ed[0] not in node_weighs:
            node_weighs[ed[0]] = 0

        node_weighs[ed[0]] += ed[2]

        if ed[1] not in node_weighs:
            node_weighs[ed[1]] = 0

        node_weighs[ed[1]] += ed[2]

    max_weight = float(max(node_weighs.values()))
    for nd in node_weighs:
        node_weighs[nd] = node_weighs[nd] / max_weight
    return {
        'node_weights':node_weighs,
        'edge_weights':edge_weights
    }


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


    print("network is connected = ", nx.is_connected(citation_net.to_undirected()))

    remove_cycles(citation_net)
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

    spc_result = spc(citation_net)
    edge_weights = spc_result['edge_weights']
    node_ids = spc_result['node_weights']

    sorted_weights = sorted(node_ids.values(), cmp=lambda x, y: (1 if y>x else -1) )
    print(" len sorted_weights=", len(sorted_weights))
    print(" len n_top_paths=", n_top_paths))
    wmin = sorted_weights[n_top_paths]
    print "wmin=", wmin
    selected_nodes = pd.DataFrame([(nd, node_ids[nd]) for nd in node_ids if node_ids[nd]>= wmin ], columns=['entryId', 'entryWeight'])
    #selected_nodes['entryId'] = selected_nodes['entryId'].map(lambda x: int(str(x)) if str(x).isdigit() else None )

    # main path analysis
    edge_distances = {}
    for ed in edge_weights:
        edge_distances[(ed[0], ed[1])] = 1.0/ed[2]

    distance_measure = lambda x,y: edge_distances[(x, y)] if (x, y) in edge_distances else 100

    reading_plan=set()
    for entryId in selected_nodes['entryId']:
        path_1 = nx.astar_path(citation_net,'s',entryId, distance_measure)
        path_2 = nx.astar_path(citation_net,entryId,'t', distance_measure)
        path_1.extend(path_2[1:])
        reading_plan.update(path_1)
        print (path_1)

    print('reading_plan')
    print(reading_plan)
    print('main path')
    print(nx.astar_path(citation_net,'s','t', distance_measure))



    selected_nodes = pd.DataFrame([(nd, node_ids[nd]) for nd in node_ids if nd in reading_plan], columns=['entryId', 'entryWeight'])
    selected_nodes['entryId'] = selected_nodes['entryId'].map(lambda x: int(str(x)) if str(x).isdigit() else None )

    snds = pd.merge(dfn0[['entryId', 'dist', 'ECC' ,'year', 'url', 'text']], selected_nodes, how='inner', left_on='entryId', right_on='entryId').sort_values(by=['entryWeight'], ascending=False)
    print snds
    fname=dataDir + '/out-citation-network-reading-plan-'+str(n_top_paths)+'-of-'+str(max_citation_net_nodes)+'-by-spc.csv'
    snds.to_csv(fname, sep="\t", quoting=csv.QUOTE_NONNUMERIC)

    print "Output is written to " + fname


    #    # create reduced network for visualisation
    #    reduced_citation_net = nx.DiGraph()
    #    for ed in selected_edges:
    #        reduced_citation_net.add_edge(ed[0], ed[1], weight=ed[2])
    #
    #    #for ed in reduced_citation_net.edges(data=True):
    #    #    print 'ed=', ed
    #
    #    nx.write_weighted_edgelist(reduced_citation_net, dataDir + "/out-citation-network-reduced.edgelist")
    #
    #    print "Reduced network is written to " + dataDir + '/out-citation-network-reduced.edgelist'
    #


'''







'''
if __name__ == "__main__":
    t0 = time.time()
    main()
    t1 = time.time()
    print "finished"
    print "time=", t1 - t0
