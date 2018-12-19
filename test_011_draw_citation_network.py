#!/usr/bin/env python2
#encoding: UTF-8

import networkx as nx
import ConfigParser
import matplotlib.pyplot as plt

# read configuration file
config = ConfigParser.ConfigParser()
config.readfp(open('config.ini'))

dataDir = config.get('main', 'dataDir')    


citation_net = nx.read_edgelist(dataDir + '/out-citation-network-reduced-to-draw.csv', create_using=nx.DiGraph() )

plt.figure( figsize=(30,20) )
#nx.draw_spring(citation_net, with_labels=True, iterations=1000)
nx.draw_spring(citation_net, with_labels=True)
#nx.draw_graphviz(citation_net, with_labels=True, iterations=1000)
plt.show()
#plt.savefig(dataDir + '/tmp-citation-network-reduced.png')