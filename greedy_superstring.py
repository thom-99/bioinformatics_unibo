import itertools 
import networkx as nx

def overlap(s1, s2):

    ovr = 0
    for i in range(1, min(len(s1), len(s2))+1):
        if s1[-i:]==s2[:i]:
            ovr = i

    return ovr

#print(overlap('atgc','gctt'))

def scs(reads:list):
    #input : list of strings 
    #output : shortest common superstring

    #creating Directed Graph using nx
    G = nx.DiGraph()
    G.add_nodes_from(reads)

    for read1, read2 in itertools.permutations(reads, 2):
        overlap_length = overlap(read1, read2)
        if overlap_length > 0:
            G.add_edge(read1, read2, overlap_length)

    #greedy alg. 

    
    
        


























