EX_GRAPH0={0:set([1,2]),
           1:set([]),
           2:set([])}

EX_GRAPH1={0:set([1,4,5]),
           1:set([2,6]),
           2:set([3]),
           3:set([0]),
           4:set([1]),
           5:set([2]),
           6:set([])
          }

EX_GRAPH2={0:set([1,4,5]),
           1:set([2,6]),
           2:set([3,7]),
           3:set([7]),
           4:set([1]),
           5:set([2]),
           6:set([]),
           7:set([3]),
           8:set([1,2]),
           9:set([0,3,4,5,6,7])
          }

def make_complete_graph(num_nodes):
    dic = {}
    list = []
    for num in range(num_nodes):
        list.append(num)
    for num in range(num_nodes):
        dic[num] = set(list).difference(set([num]))
        
    return dic

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

print compute_in_degrees(EX_GRAPH2)
print in_degree_distribution(EX_GRAPH2)

