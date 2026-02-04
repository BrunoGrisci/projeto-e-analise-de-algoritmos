from typing import Dict, List, Hashable

def eulerian_path(graph: Dict[Hashable, List[Hashable]], start: Hashable) -> List[Hashable]:
    """
    Compute an Eulerian path in a directed graph using an explicit stack.
    
    Parameters
    ----------
    graph : dict
        A dictionary mapping each vertex to a list of vertices it has
        outgoing edges to. Example:
        G = {
            'A': ['B'],
            'B': ['C'],
            'C': ['A'],
        }
        The graph is assumed to have an Eulerian path starting at `start`.
        This function does not check the Eulerian conditions.
    
    start : hashable
        The starting vertex for the Eulerian path.
    
    Returns
    -------
    path : list
        A list of vertices in the order they appear along the Eulerian path.
    """
    # Make a local copy of adjacency lists so we can mutate them
    adj = {v: list(neigh) for v, neigh in graph.items()}
    
    # Make sure every vertex that appears as a target also has an entry
    for v in list(adj):
        for u in adj[v]:
            if u not in adj:
                adj[u] = []

    stack = [start]
    path: List[Hashable] = []

    while stack:
        v = stack[-1]  # value at the top of the stack
        if adj[v]:
            # "find any edge coming out of V" – take one outgoing edge
            u = adj[v].pop()   # remove this edge from the graph
            stack.append(u)    # push the second end in the stack
        else:
            # degree(V) == 0
            path.append(stack.pop())  # add V to the answer and pop it

    # We built the path in reverse
    path.reverse()
    return path

if __name__ == "__main__":

    G = {
        'A': ['B'],
        'B': ['F'],
        'C': ['D'],
        'D': ['H'],
        'E':['A'],
        'F':['E', 'G'],
        'G':['C', 'J'],
        'H':['G'],
        'I':['F'],
        'J':['I'],

    }

    start = 'A'
    p = eulerian_path(G, start)
    print(p)  

    Gsemi = {
        'Z': ['D'],
        'A': ['B'],
        'B': ['F'],
        'C': ['D'],
        'D': ['H'],
        'E':['A'],
        'F':['E', 'G'],
        'G':['C', 'J'],
        'H':['G'],
        'I':['F'],
        'J':['I'],

    }

    start = 'Z'
    p = eulerian_path(Gsemi, start)
    print(p)  