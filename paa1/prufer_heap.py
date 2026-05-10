#!/usr/bin/env python3
"""
Codigo de Prüfer usando heap minimo.

O codigo de Prüfer representa uma arvore rotulada com vertices
1, 2, ..., n por uma sequencia de n - 2 rotulos.

Este arquivo implementa:

- prufer_encode_heap(tree): codificacao em O(n log n)
- prufer_decode_heap(code): decodificacao em O(n log n)

A heap guarda sempre as folhas disponiveis. Como cada extracao ou insercao
na heap custa O(log n), e fazemos O(n) operacoes desse tipo, o tempo total
fica O(n log n). As varreduras iniciais de graus e os testes de validade
custam O(n) em uma arvore, logo nao mudam a ordem assintotica dominante.

Representacao usada:

tree = {
    1: [4, 7, 8],
    2: [7],
    ...
}

O grafo e nao direcionado: se u aparece em tree[v], entao v tambem deve
aparecer em tree[u].
"""

from collections import deque
import heapq
from typing import Dict, Iterable, List, Sequence, Set, Tuple


Tree = Dict[int, List[int]]
Edge = Tuple[int, int]


def _validate_and_copy_tree(tree: Dict[int, Iterable[int]]) -> Tree:
    """
    Valida se a entrada e uma arvore com vertices 1, ..., n.

    A funcao tambem faz uma copia das listas de adjacencia para que os
    algoritmos possam consultar a arvore sem modificar a estrutura recebida.

    Custo: O(n), pois uma arvore tem n - 1 arestas.
    """
    n = len(tree)
    if n < 2:
        raise ValueError("O codigo de Prüfer usado aqui assume n >= 2.")

    expected_vertices = set(range(1, n + 1))
    if set(tree) != expected_vertices:
        raise ValueError("Os vertices devem ser exatamente 1, 2, ..., n.")

    adjacency_sets: Dict[int, Set[int]] = {}
    for vertex in range(1, n + 1):
        neighbors = list(tree[vertex])
        if len(neighbors) != len(set(neighbors)):
            raise ValueError(f"O vertice {vertex} possui vizinhos repetidos.")
        adjacency_sets[vertex] = set(neighbors)

    edges: Set[Edge] = set()
    for vertex in range(1, n + 1):
        for neighbor in adjacency_sets[vertex]:
            if neighbor not in expected_vertices:
                raise ValueError(f"Vizinho invalido: {neighbor}.")
            if neighbor == vertex:
                raise ValueError("A arvore nao pode ter lacos.")
            if vertex not in adjacency_sets[neighbor]:
                raise ValueError("A lista de adjacencia deve ser simetrica.")
            edges.add((min(vertex, neighbor), max(vertex, neighbor)))

    if len(edges) != n - 1:
        raise ValueError("Uma arvore com n vertices deve ter exatamente n - 1 arestas.")

    visited = {1}
    queue: deque[int] = deque([1])
    while queue:
        vertex = queue.popleft()
        for neighbor in adjacency_sets[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    if len(visited) != n:
        raise ValueError("O grafo precisa ser conexo para ser uma arvore.")

    return {vertex: list(adjacency_sets[vertex]) for vertex in range(1, n + 1)}


def _validate_and_copy_code(code: Sequence[int]) -> List[int]:
    """
    Valida uma sequencia de Prüfer e devolve uma copia como lista.

    Se o codigo tem tamanho n - 2, entao a arvore decodificada tem n vertices.
    Portanto todos os simbolos precisam pertencer ao alfabeto {1, ..., n}.

    Custo: O(n).
    """
    prufer_code = list(code)
    n = len(prufer_code) + 2

    for label in prufer_code:
        if not isinstance(label, int):
            raise ValueError("Todos os rotulos do codigo devem ser inteiros.")
        if label < 1 or label > n:
            raise ValueError(f"Rotulo {label} fora do intervalo 1, ..., {n}.")

    return prufer_code


def prufer_encode_heap(tree: Dict[int, Iterable[int]]) -> List[int]:
    """
    Codifica uma arvore rotulada pelo codigo de Prüfer em O(n log n).

    Ideia do algoritmo:

    1. Calculamos o grau atual de cada vertice.
    2. Inserimos todas as folhas em uma heap minima.
    3. Repetimos n - 2 vezes:
       - removemos da heap a menor folha f;
       - encontramos seu unico vizinho ainda presente, chamado g;
       - adicionamos g ao codigo;
       - removemos f da arvore apenas pelo vetor de graus;
       - se g virou folha, inserimos g na heap.

    A heap garante que a folha escolhida em cada passo e sempre a de menor
    rotulo, exatamente como na definicao do codigo de Prüfer.
    """
    adjacency = _validate_and_copy_tree(tree)
    n = len(adjacency)

    degree = [0] * (n + 1)
    for vertex in range(1, n + 1):
        degree[vertex] = len(adjacency[vertex])

    leaves = [vertex for vertex in range(1, n + 1) if degree[vertex] == 1]
    heapq.heapify(leaves)

    code: List[int] = []

    for _ in range(n - 2):
        leaf = heapq.heappop(leaves)

        # A folha atual tem exatamente um vizinho ainda nao removido.
        parent = None
        for neighbor in adjacency[leaf]:
            if degree[neighbor] > 0:
                parent = neighbor
                break

        if parent is None:
            raise RuntimeError("Entrada invalida: folha sem vizinho ativo.")

        code.append(parent)

        # Remover a folha fisicamente da lista seria caro. Basta atualizar graus:
        # vertices com grau 0 sao tratados como removidos.
        degree[leaf] = 0
        degree[parent] -= 1

        if degree[parent] == 1:
            heapq.heappush(leaves, parent)

    return code


def prufer_decode_heap(code: Sequence[int]) -> Tree:
    """
    Decodifica um codigo de Prüfer em uma arvore em O(n log n).

    Em um codigo de Prüfer, o grau final de um vertice v e:

        grau(v) = 1 + numero de ocorrencias de v no codigo.

    Assim, os vertices que nao aparecem no codigo sao folhas. A cada simbolo x
    do codigo, conectamos a menor folha disponivel a x. Depois reduzimos o grau
    de x; se x virar folha, ele entra na heap.
    """
    prufer_code = _validate_and_copy_code(code)
    n = len(prufer_code) + 2

    degree = [1] * (n + 1)
    degree[0] = 0
    for label in prufer_code:
        degree[label] += 1

    leaves = [vertex for vertex in range(1, n + 1) if degree[vertex] == 1]
    heapq.heapify(leaves)

    tree: Tree = {vertex: [] for vertex in range(1, n + 1)}

    for label in prufer_code:
        leaf = heapq.heappop(leaves)

        tree[leaf].append(label)
        tree[label].append(leaf)

        degree[leaf] = 0
        degree[label] -= 1

        if degree[label] == 1:
            heapq.heappush(leaves, label)

    first_leaf = heapq.heappop(leaves)
    second_leaf = heapq.heappop(leaves)
    tree[first_leaf].append(second_leaf)
    tree[second_leaf].append(first_leaf)

    return tree


def tree_edges(tree: Dict[int, Iterable[int]]) -> Set[Edge]:
    """Devolve o conjunto de arestas nao direcionadas de uma arvore."""
    edges: Set[Edge] = set()
    for vertex, neighbors in tree.items():
        for neighbor in neighbors:
            edges.add((min(vertex, neighbor), max(vertex, neighbor)))
    return edges


def make_tree(n: int, edges: Iterable[Edge]) -> Tree:
    """Monta uma lista de adjacencia a partir de uma lista de arestas."""
    tree: Tree = {vertex: [] for vertex in range(1, n + 1)}
    for vertex, neighbor in edges:
        tree[vertex].append(neighbor)
        tree[neighbor].append(vertex)
    return tree


def _run_tests() -> None:
    """Casos de teste simples, executados com `python3 prufer_heap.py`."""
    two_vertices = make_tree(2, [(1, 2)])
    assert prufer_encode_heap(two_vertices) == []
    assert tree_edges(prufer_decode_heap([])) == tree_edges(two_vertices)

    path = make_tree(4, [(1, 2), (2, 3), (3, 4)])
    assert prufer_encode_heap(path) == [2, 3]
    assert tree_edges(prufer_decode_heap([2, 3])) == tree_edges(path)

    star = make_tree(5, [(4, 1), (4, 2), (4, 3), (4, 5)])
    assert prufer_encode_heap(star) == [4, 4, 4]
    assert tree_edges(prufer_decode_heap([4, 4, 4])) == tree_edges(star)

    slide_tree = make_tree(
        8,
        [
            (2, 7),
            (7, 1),
            (1, 4),
            (4, 3),
            (7, 6),
            (1, 8),
            (4, 5),
        ],
    )
    slide_code = [7, 4, 4, 1, 7, 1]
    assert prufer_encode_heap(slide_tree) == slide_code
    assert tree_edges(prufer_decode_heap(slide_code)) == tree_edges(slide_tree)

    exercise_code = [2, 3, 9, 5, 1, 8, 5, 2]
    exercise_tree = prufer_decode_heap(exercise_code)
    assert prufer_encode_heap(exercise_tree) == exercise_code

    try:
        prufer_encode_heap({1: [2], 2: [1], 3: []})
    except ValueError:
        pass
    else:
        raise AssertionError("Um grafo desconexo nao deve ser aceito.")

    print("Todos os testes da versao com heap passaram.")


if __name__ == "__main__":
    _run_tests()

    print(prufer_encode_heap({1:[4,7,8],
                              2:[7],
                              3:[4],
                              4:[1,3,5],
                              5:[4],
                              6:[7],
                              7:[1,2,6],
                              8:[1]}))
    
    print(prufer_decode_heap([7, 4, 4, 1, 7, 1]))
    print(prufer_decode_heap([2, 3, 9, 5, 1, 8, 5, 2]))

