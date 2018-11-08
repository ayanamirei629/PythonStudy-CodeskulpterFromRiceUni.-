"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import urllib2


# Set timeout for CodeSkulptor if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph



def compute_in_degrees(digraph):
    dic_in_degree = dict(digraph)
    for key in dic_in_degree.keys():
        dic_in_degree[key] = 0
    for value in digraph.values():
        for val in list(value):
            dic_in_degree[val] += 1
    return dic_in_degree     

def in_degree_distribution(digraph):
    dic_degree_distribution = {}
    dic_in_degree = dict(compute_in_degrees(digraph))
    for value in dic_in_degree.values():
        if dic_degree_distribution.get(value) == None:
            dic_degree_distribution[value] = 0
        dic_degree_distribution[value] += 1/(float(len(digraph)))
    return dic_degree_distribution

citation_graph = load_graph(CITATION_URL)
distribution = dict(in_degree_distribution(citation_graph))

total = 0
print distribution


import simpleplot
#simpleplot.plot_lines('HOMEWORK1', 400, 300, 'in degree nodes', 'distribution', [distribution])