import itertools 
import networkx as nx
import random

def overlap(s1, s2):

    ovr = 0
    for i in range(1, min(len(s1), len(s2))+1):
        if s1[-i:]==s2[:i]:
            ovr = i

    return ovr

#print(overlap('atgc','gctt'))

def digraph(reads:list):
    #input : list of 
    # #output : directed graph with w. edges  

    #creating Directed Graph using nx
    G = nx.DiGraph()
    G.add_nodes_from(reads)

    for read1, read2 in itertools.permutations(reads, 2):
        overlap_length = overlap(read1, read2)
        if overlap_length > 0:
            G.add_edge(read1, read2, weight=overlap_length)

    return G

#g = digraph(["ATTAGACCTG", "CCTGCCGGAA", "AGACCTGCCG", "GCCGGAATAC"])

def scs(reads:list):
    
    G = digraph(reads)

    #chosing a random node to start with 
    current_node = random.choice(list(G.nodes))

    visited_nodes = {current_node}
    superstring = current_node

    while len(visited_nodes) < len(G.nodes):
        next_node = None
        max_overlap = 0

        #successors in this digraph are nodes with which there is some overlap
        for successor in G.successors(current_node):
            if successor not in visited_nodes:
                #getting the weight = overlap between the two nodes
                current_overlap = G[current_node][successor]['weight']
                if current_overlap > max_overlap:
                    max_overlap = current_overlap
                    next_node = successor
        
        #if there are no nodes with overlaop i.e. no successors 
        if next_node == None:
            #we use the properties of a set to pick a random unvisited node
            unvisited_nodes = set(G.nodes) - visited_nodes
            #if unvisited_nodes is not empty
            if unvisited_nodes:
                next_node = random.choice(list(unvisited_nodes))
                superstring += next_node
            else:
                break
        
        else:
            superstring += next_node[max_overlap:]

        visited_nodes.add(next_node)
        current_node = next_node

    return superstring


print(scs(["ATTAGACCTG", "CCTGCCGGAA", "AGACCTGCCG", "GCCGGAATAC"]))






