# Projeto e Análise de Algoritmos I
# Distância em grafos valorados.
# Bruno Iochins Grisci e Rodrigo Machado
# Universidade Federal do Rio Grande do Sul
# Instituto de Informática
# Departamento de Informática Teórica
# https://en.wikipedia.org/wiki/Greedy_coloring

def first_available(colors):
    """
    Return the smallest non-negative integer not in the given set of colors.
    """
    color = 0
    while color in colors:
        color += 1
    return color


def greedy_coloring(G, order):
    """
    Find the greedy coloring of G in the given vertex order.
    """
    coloring = {}
    for node in order:
        used_neighbour_colors = {
            coloring[nbr] for nbr in G[node] if nbr in coloring
        }
        coloring[node] = first_available(used_neighbour_colors)
    return coloring


def welsh_powell_order(G):
    """
    Vertices sorted in non-increasing order of degree.
    """
    return sorted(G.keys(), key=lambda v: len(G[v]), reverse=True)


def print_graph(G):
    """
    Print the graph in a clean, readable form.
    """
    print("Graph (adjacency list):")
    for v in sorted(G.keys()):
        print(f"  {v}: {G[v]}")
    print()


def main():
    # Example graph
    Gexemp = {
        'A': ['B', 'C', 'D'],
        'B': ['A', 'C', 'E'],
        'C': ['A', 'B', 'D', 'E'],
        'D': ['A', 'C'],
        'E': ['B', 'C', 'F'],
        'F': ['E'],
    }


    crown_graph = {
        'L1': ['R2', 'R3', 'R4'],
        'L2': ['R1', 'R3', 'R4'],
        'L3': ['R1', 'R2', 'R4'],
        'L4': ['R1', 'R2', 'R3'],        
        'R1': ['L2', 'L3', 'L4'],
        'R2': ['L1', 'L3', 'L4'],
        'R3': ['L1', 'L2', 'L4'],
        'R4': ['L1', 'L2', 'L3'],
    }

    fail_graph = {
    'a':['b','f','g'],
    'b':['a','c'],
    'c':['b','d'],
    'd':['c','e','h'],
    'e':['d','f'],
    'f':['e','a'],
    'g':['a'],
    'h':['d'],
    }

    G = crown_graph

    # Print the graph
    print_graph(G)

    # Compute Welsh–Powell ordering
    order = welsh_powell_order(G)

    # Build a list with degrees for printing
    order_with_degrees = [(v, len(G[v])) for v in order]

    print("Welsh–Powell vertex order (with degrees):")
    print("  " + ", ".join(f"{v}(deg={d})" for v, d in order_with_degrees))
    print()

    # Compute greedy coloring
    coloring = greedy_coloring(G, order)

    # Print vertex colors
    print("Vertex coloring:")
    for v in sorted(coloring.keys()):
        print(f"  {v}: color {coloring[v]}")

    # Number of colors used
    num_colors = max(coloring.values()) + 1 if coloring else 0
    print(f"\nNumber of colors used: {num_colors}")


if __name__ == "__main__":
    main()

