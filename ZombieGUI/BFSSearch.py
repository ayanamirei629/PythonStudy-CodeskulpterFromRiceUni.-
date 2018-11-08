"""
Breadth-first search
"""
def cc_visited(ugraph):
    """
    Takes the undirected graph  and returns a list 
    of sets, where each set consists of all the nodes 
    (and nothing else) in a connected component,
    and there is exactly one set in the list for each
    connected component in  and nothing else.
    """
#put all nodes into their own sets first
    list_of_set = []
    for node in ugraph:
        temp_set = set()
        for set_index in ugraph[node]:
            temp_set.add(set_index)
        temp_set.add(node)
        list_of_set.append(temp_set)
#combine sets if they have same node
    position = 0
    while position < len(list_of_set):
        node = 1
        while node < len(list_of_set) - position:
            if list_of_set[position].intersection(list_of_set[node + position]) != set([]):
                list_of_set[position] = list_of_set[position].union(list_of_set[node + position])
                list_of_set.remove(list_of_set[node + position])
                node -= 1
            node += 1 
        position +=1    
    return list_of_set


def largest_cc_size(ugraph):
    """
    Takes the undirected graph  and returns 
    the size (an integer) of the largest connected
    component in 
    """
    #put all nodes into their own sets first
    list_of_set = cc_visited(ugraph)
    for node in range(len(list_of_set)):
        list_of_set[node] = len(list_of_set[node])
    return max(list_of_set)    

def bfs_visited(ugraph, start_node):
    """
    Takes the undirected graph  and 
    the node  and returns the set 
    consisting of all nodes 
    that are visited by a breadth-first 
    search that starts at .
    """
    bfs_list = cc_visited(ugraph)
    for bfs_set in bfs_list:
        for bfs_node in bfs_set:
            if bfs_node == start_node: 
                return bfs_set

def remove_node(ugraph, attack_node):
    """
    """
 
    for key in ugraph:
        if key == attack_node:
            ugraph.pop(key)
        else:
            for value in ugraph[key]:
                if value == attack_node:
                    ugraph[key].discard(attack_node)
    return ugraph

def compute_resilience(ugraph, attack_order):
    """
    Takes the undirected graph ugraph, a list of nodes attack_order and iterates
    through the nodes in attack_order.
    """
    temp_ugraph = dict(ugraph)
    temp_largest = []
    temp_largest.append(largest_cc_size(temp_ugraph))
    for attack_node in attack_order:
        temp_largest.append(largest_cc_size(remove_node(temp_ugraph,attack_node)))
    return temp_largest

        
            