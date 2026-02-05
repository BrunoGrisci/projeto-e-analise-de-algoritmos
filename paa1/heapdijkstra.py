# Projeto e Análise de Algoritmos I
# Distância em grafos valorados.
# Bruno Iochins Grisci e Rodrigo Machado
# Universidade Federal do Rio Grande do Sul
# Instituto de Informática
# Departamento de Informática Teórica

from typing import Dict, Hashable, List, Tuple, Optional
import heapq
import random
import time

Weight = float
Node = Hashable
Adj = Dict[Node, List[Tuple[Node, Weight]]]

def generate_random_graph(n: int,
                          avg_degree: int = 6,
                          weight_low: int = 1,
                          weight_high: int = 10,
                          directed: bool = False,
                          seed: Optional[int] = None) -> Adj:
    """
    Generate a random graph with strictly positive weights using the same adjacency format
    used in the examples. All nodes appear as keys. Optionally ensures connectivity by
    first adding a random spanning tree, then sprinkling extra edges.

    Parameters
    ----------
    n : int
        Number of nodes (v0, v1, ..., v{n-1}).
    avg_degree : int, optional
        Desired average out-degree per node (approximate).
    weight_low, weight_high : int, optional
        Inclusive range for integer positive weights.
    directed : bool, optional
        If False, add symmetric edges (undirected as two directed arcs).
    seed : Optional[int], optional
        Random seed for reproducibility.

    Returns
    -------
    Adj
        Adjacency dict: node -> list of (neighbor, positive_weight).
    """
    assert n >= 1, "n must be >= 1"
    if seed is not None:
        random.seed(seed)

    nodes = [f'v{i}' for i in range(n)]
    graph: Adj = {u: [] for u in nodes}

    # Helper to add an edge if not duplicate and not self-loop
    def add_edge(u: Node, v: Node, w: int):
        if u == v:
            return
        # prevent duplicate (u,v)
        if not any(x == v for (x, _) in graph[u]):
            graph[u].append((v, float(w)))

    # 1) Build a random spanning tree to ensure connectivity (n-1 edges)
    for i in range(1, n):
        u = nodes[i]
        v = nodes[random.randrange(0, i)]  # connect to a previous node
        w = random.randint(weight_low, weight_high)
        add_edge(u, v, w)
        if not directed:
            add_edge(v, u, w)

    # 2) Sprinkle additional edges to reach target density
    # total target edges (outgoing count) ~ n * avg_degree
    current_edges = sum(len(adj) for adj in graph.values())
    target_edges = max(n - 1, n * avg_degree)
    attempts = 0
    max_attempts = 10 * (target_edges - current_edges + 1)

    while current_edges < target_edges and attempts < max_attempts:
        u = random.choice(nodes)
        v = random.choice(nodes)
        if u != v:
            w = random.randint(weight_low, weight_high)
            before = len(graph[u])
            add_edge(u, v, w)
            after = len(graph[u])
            if after > before:
                current_edges += 1
                if not directed:
                    # Add symmetric edge if it didn't exist
                    before2 = len(graph[v])
                    add_edge(v, u, w)
                    if len(graph[v]) > before2:
                        current_edges += 1
        attempts += 1

    return graph

def dijkstra_heap(graph: Adj, source: Node) -> Tuple[Dict[Node, Weight], Dict[Node, Optional[Node]]]:
    """
    Dijkstra with a binary heap priority queue.
    Time complexity: O(|E| + |V| log |V|) for standard adjacency-list graphs with non-negative weights.

    Parameters
    ----------
    graph : Adj
        Adjacency dictionary where graph[u] is a list of (v, w) edges.
    source : Node
        Source node.

    Returns
    -------
    dist : Dict[Node, Weight]
        Shortest-path distance from source to each node (float('inf') if unreachable).
    parent : Dict[Node, Optional[Node]]
        Predecessor on a shortest path tree (None for source and unreachable nodes).

    Notes
    -----
    - Requires non-negative edge weights.
    - This version uses a min-heap (heapq). We allow multiple entries per node
      in the heap and skip "stale" ones by checking if the popped distance
      matches the current dist[u].
    """
    # Ensure the source exists as a key
    if source not in graph:
        graph = {**graph, source: graph.get(source, [])}

    # Collect all nodes (include those that only appear as targets)
    nodes = set(graph.keys())
    for u, outs in graph.items():
        for v, w in outs:
            nodes.add(v)

    dist: Dict[Node, Weight] = {v: float('inf') for v in nodes}
    parent: Dict[Node, Optional[Node]] = {v: None for v in nodes}
    dist[source] = 0.0

    # Min-heap of (distance, node)
    heap: List[Tuple[Weight, Node]] = [(0.0, source)]
    heapq.heapify(heap)

    visited = set()

    ########### LAÇO PRINCIPAL

    while heap:     
        du, u = heapq.heappop(heap)
        if u in visited:
            continue
        # Skip stale pair (lazy decrease-key)
        if du != dist[u]:
            continue

        visited.add(u)

        # Relax outgoing edges
        for v, w in graph.get(u, []):
            if w < 0:
                raise ValueError("Dijkstra requires non-negative weights.")
                '''
                The classic “naive” Dijkstra variants typically do a fixed number of relaxations (e.g.,∣V∣−1 outer passes or a loop that stops after visiting each vertex once). 
                Even with negative edges or negative cycles, this loop still ends, though the results may be wrong.

                The heap-based version keeps processing until the priority queue (heap) is empty.
                With negative cycles reachable from the source, a node’s tentative distance can keep getting reduced again and again (unbounded below), so the heap keeps receiving “better” keys 
                and never empties.
                '''
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(heap, (nd, v))

    return dist, parent


def reconstruct_path(parent: Dict[Node, Optional[Node]], dist: Dict[Node, Weight], target: Node) -> List[Node]:
    """
    Reconstructs the path to 'target' using 'parent'.
    Returns [] if 'target' is unreachable.
    """
    # Unreachable (and not the source) if distance is inf
    if dist.get(target, float('inf')) == float('inf'):
        return []

    path: List[Node] = []
    cur: Optional[Node] = target
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path


if __name__ == "__main__":
    # Directed example
    if False:
        G = {
            's': [('a', 1), ('b', 4)],
            'a': [('b', 2), ('c', 5)],
            'b': [('c', 1)],
            'c': []
        }
        dist, parent = dijkstra_heap(G, 's')
        print("dist:", dist)
        print("parent:", parent)
        print("caminho s->c:", reconstruct_path(parent, dist, 'c'))
        print('\n\n\n')

    if True:
        GExemp = {
            'S': [('A', 1), ('B', 3)],
            'A': [('S', 1), ('D', 5), ('C', 4)],
            'B': [('S', 3), ('D', 4), ('C', 1)],
            'C': [('B', 1), ('A', 4), ('E', 6)],
            'D': [('A', 5), ('B', 4), ('E', 2)],
            'E': [('D', 2), ('C', 6)],
            'F': [],
        }

        print("graph:", GExemp)
        dist, parent = dijkstra_heap(GExemp, 'S')
        print("dist:", dist)
        print("parent:", parent)
        print("caminho S->E:", reconstruct_path(parent, dist, 'E'))
        print("caminho S->S:", reconstruct_path(parent, dist, 'S'))
        print("caminho S->F:", reconstruct_path(parent, dist, 'F'))
        print('\n\n\n')


    if True:
        for n in [100, 1_000, 10_000, 100_000, 1_000_000]:
            # === Benchmark on a random positive-weight graph ===
            avg_deg = 6     # average out-degree
            seed = 42       # for reproducibility
            directed = False

            G = generate_random_graph(n, avg_degree=avg_deg, weight_low=1, weight_high=10,
                                      directed=directed, seed=seed)
            src = 'v0'

            # Time heap-based Dijkstra
            t0 = time.perf_counter()
            dist_heap, parent_heap = dijkstra_heap(G, src)
            t1 = time.perf_counter()

            print(f"\n=== Timing (n={n}, avg_deg={avg_deg}, directed={directed}) ===")
            print(f"Heap Dijkstra:   {t1 - t0:.6f} s")