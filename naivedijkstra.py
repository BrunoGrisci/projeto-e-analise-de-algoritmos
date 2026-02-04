# Projeto e Análise de Algoritmos I
# Distância em grafos valorados.
# Bruno Iochins Grisci e Rodrigo Machado
# Universidade Federal do Rio Grande do Sul
# Instituto de Informática
# Departamento de Informática Teórica

from typing import Dict, Hashable, List, Tuple, Optional

Weight = float
Node = Hashable
Adj = Dict[Node, List[Tuple[Node, Weight]]]
import random
import time

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

def dijkstra_naive(graph: Adj, source: Node) -> Tuple[Dict[Node, Weight], Dict[Node, Optional[Node]]]:
    """
    Dijkstra O(|V||E|) sem fila de prioridades.

    Ideia:
      - Mantemos um conjunto S de vértices "finalizados" (visitados).
      - Em cada iteração, escolhemos o próximo vértice u* fora de S cuja
        distância dist[u*] é mínima entre todas as arestas que "cruzam o corte"
        (vértices em S -> vértices não em S).
      - Para encontrar u*, varremos TODAS as arestas do grafo (custo O(|E|) por iteração).
      - Repetimos por até |V| iterações, totalizando O(|V||E|).

    Pré-condições:
      - Pesos não-negativos.
      - O grafo é representado como um dicionário: graph[u] = [(v, w), ...].

    Parâmetros:
      graph: adjacência dirigida (ou use arestas duplicadas para grafo não dirigido).
      source: nó de origem.

    Retorna:
      dist: dicionário com a menor distância da origem para cada nó.
            Para nós inalcançáveis, distância = float('inf').
      parent: dicionário com o predecessor imediato no caminho mínimo
              (None para a origem e para nós inalcançáveis).

    Complexidade:
      Seleção do próximo vértice: O(|E|) por iteração.
      Até |V| iterações => O(|V||E|). Relaxamentos somam O(|E|), mas não dominam.

    Exemplo de uso:
      G = {
          's': [('a', 1), ('b', 4)],
          'a': [('b', 2), ('c', 5)],
          'b': [('c', 1)],
          'c': []
      }
      dist, parent = dijkstra_ve(G, 's')

    Observações:
      - Este código evita estruturas avançadas (como heap/fila de prioridade)
        para destacar a lógica do algoritmo e a análise de complexidade.
      - Para tornar O((|V|+|E|) log |V|), usa-se uma fila de prioridades (heap).
    """
    # Verificações básicas
    if source not in graph:
        # Garante que todos os nós apareçam como chave (mesmo sem saída)
        graph = {**graph, source: graph.get(source, [])}

    # Coletar o conjunto de nós (em caso de nós que só apareçam como destino)
    nodes = set(graph.keys())
    for u, outs in graph.items():
        for v, w in outs:
            #if w < 0:
            #    raise ValueError("Dijkstra requer pesos não negativos.")
            #Erro removido por razões didáticas.
            nodes.add(v)

    # Inicializações
    dist: Dict[Node, Weight] = {v: float('inf') for v in nodes}
    parent: Dict[Node, Optional[Node]] = {v: None for v in nodes}
    visited: Dict[Node, bool] = {v: False for v in nodes}

    dist[source] = 0.0
    visited_count = 0

    # Pré-construir lista de arestas para facilitar a varredura O(|E|)
    edges: List[Tuple[Node, Node, Weight]] = []
    for u, outs in graph.items():
        for v, w in outs:
            edges.append((u, v, w))

    ########### LAÇO PRINCIPAL

    # Laço principal: até visitar todos ou não haver mais alcançáveis
    while visited_count < len(nodes):
        # Escolha do próximo vértice via varredura de TODAS as arestas (corte S -> V\S)
        next_node = None
        next_dist = float('inf')

        # Se ainda não temos nenhum visitado, começamos pela origem
        # (garantido pelo dist[source] = 0 e pelas regras abaixo)
        for (u, v, w) in edges:
            if visited[u] and not visited[v]:
                cand = dist[u] + w
                if cand < next_dist:
                    next_dist = cand
                    next_node = v

        # Caso inicial: quando S está vazio (ninguém visitado ainda),
        # selecionamos a origem manualmente.
        if visited_count == 0:
            next_node = source
            next_dist = 0.0

        # Se não há próximo alcançável (componente desconexo), encerramos
        if next_node is None:
            break

        # "Finaliza" o próximo nó
        visited[next_node] = True
        visited_count += 1

        # A distância mínima encontrada para next_node está consolidada
        if dist[next_node] > next_dist:
            dist[next_node] = next_dist  # normaliza caso tenha vindo do corte

        # Relaxa arestas que saem de next_node (opcional; acelera convergência local)
        for (v, w) in graph.get(next_node, []):
            if not visited[v] and dist[next_node] + w < dist[v]:
                dist[v] = dist[next_node] + w
                parent[v] = next_node

        # Também é possível atualizar parents quando definimos next_node a partir do corte.
        # Para isso, buscamos quem gerou next_dist (apenas uma passagem O(|E|)):
        # (Fazemos isso apenas quando next_node não é a origem.)
        if next_node != source:
            best_parent = parent[next_node]  # pode já ter sido definido
            best_val = dist[next_node]
            # Reconfirma pai via corte (apenas se houver melhora)
            for (u, v, w) in edges:
                if v == next_node and visited[u]:
                    cand = dist[u] + w
                    if cand <= best_val + 1e-15:  # tolerância numérica
                        best_val = cand
                        best_parent = u
            parent[next_node] = best_parent

    return dist, parent


def reconstruct_path(parent: Dict[Node, Optional[Node]], target: Node) -> List[Node]:
    """
    Reconstrói o caminho até 'target' usando o dicionário 'parent'.
    Retorna [] se 'target' for inalcançável (parent[target] é None e não é a origem).
    """
    
    if dist[target] == 0.0:
        return [target]

    path: List[Node] = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    # Se não há pai e o caminho tem 1 nó, pode ser origem ou inalcançável:
    # O chamador pode checar dist[target] para decidir.
    if len(path) > 1:
        return path
    else:
        return []


if __name__ == "__main__":
    
    # Exemplo dirigido
    if False:
        G = {
            's': [('a', 1), ('b', 4)],
            'a': [('b', 2), ('c', 5)],
            'b': [('c', 1)],
            'c': []
        }
        dist, parent = dijkstra_naive(G, 's')
        print("dist:", dist)
        print("parent:", parent)
        print("caminho s->c:", reconstruct_path(parent, 'c'))
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
        dist, parent = dijkstra_naive(GExemp, 'S')
        print("dist:", dist)
        print("parent:", parent)
        print("caminho S->E:", reconstruct_path(parent, 'E'))
        print("caminho S->S:", reconstruct_path(parent, 'S'))
        print("caminho S->F:", reconstruct_path(parent, 'F'))
        print('\n\n\n')

    if False:
        GNeg1 = {
            'A': [('B', 8)],
            'B': [('D', -2), ('E', 2)],
            'C': [],
            'D': [('E', 2)],
            'E': [('B', 2), ('D', 2), ('F', 2)],
            'F': [],
        }

        print("graph:", GNeg1)
        dist, parent = dijkstra_naive(GNeg1, 'A')
        print("dist:", dist)
        print("parent:", parent)
        print("caminho A->F:", reconstruct_path(parent, 'F'))
        print('\n\n\n')

    if False:
        GNeg2 = {
            'A': [('B', 8)],
            'B': [('D', 4), ('E', 2)],
            'C': [],
            'D': [('B', 4), ('E', -5)],
            'E': [('B', 2), ('F', 2)],
            'F': [],
        }

        print("graph:", GNeg2)
        dist, parent = dijkstra_naive(GNeg2, 'A')
        print("dist:", dist)
        print("parent:", parent)
        print("caminho A->F:", reconstruct_path(parent, 'F'))
        print('\n\n\n')

    if False:
        GNeg3 = {
            'A': [('D', -30)],
            'B': [('A', 8)],
            'C': [],
            'D': [('E', 10)],
            'E': [('B', 2), ('F', 2)],
            'F': [],
        }

        print("graph:", GNeg3)
        dist, parent = dijkstra_naive(GNeg3, 'A')
        print("dist:", dist)
        print("parent:", parent)
        print("caminho A->F:", reconstruct_path(parent, 'F'))
        print('\n\n\n')

    if False:
        for n in [100, 1_000, 10_000, 100_000]:
            # === Benchmark on a random positive-weight graph ===
            avg_deg = 6     # average out-degree
            seed = 42       # for reproducibility
            directed = False

            G = generate_random_graph(n, avg_degree=avg_deg, weight_low=1, weight_high=10,
                                      directed=directed, seed=seed)
            src = 'v0'

            # Time naive Dijkstra
            t0 = time.perf_counter()
            dist_heap, parent_heap = dijkstra_naive(G, src)
            t1 = time.perf_counter()

            print(f"\n=== Timing (n={n}, avg_deg={avg_deg}, directed={directed}) ===")
            print(f"Naive Dijkstra:   {t1 - t0:.6f} s")