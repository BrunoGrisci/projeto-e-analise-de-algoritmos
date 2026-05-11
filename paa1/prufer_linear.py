#!/usr/bin/env python3
"""
Codigo de Prüfer em tempo linear.

O codigo de Prüfer representa uma arvore rotulada com vertices
1, 2, ..., n por uma sequencia de n - 2 rotulos.

Este arquivo implementa:

- prufer_encode_linear(tree): codificacao em O(n)
- prufer_decode_linear(code): decodificacao em O(n)

A diferenca central para a versao com heap e a escolha da menor folha.
Em vez de manter uma fila de prioridade, usamos:

1. um vetor degree[v] com o grau atual de cada vertice;
2. um ponteiro monotonicamente crescente que procura a proxima folha;
3. uma variavel leaf, que pode receber imediatamente uma nova folha menor
   que o ponteiro atual.

Quando a remocao de uma folha faz seu vizinho virar folha e esse vizinho tem
rotulo menor que o ponteiro, ele deve ser processado imediatamente. Caso
contrario, o ponteiro continua andando para a direita ate encontrar a proxima
folha. Como o ponteiro nunca volta, o custo total das buscas e O(n).

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


def _first_leaf_from(degree: List[int], start: int) -> int:
    """
    Procura a primeira posicao >= start cujo grau atual e 1.

    Na codificacao e na decodificacao lineares, essa funcao e chamada com
    valores de start que nunca diminuem. Logo, somadas ao longo de todo o algoritmo,
    as posicoes puladas custam O(n), nao O(n^2).
    """
    pointer = start
    while pointer < len(degree) and degree[pointer] != 1:
        pointer += 1
    return pointer


def prufer_encode_linear(tree: Dict[int, Iterable[int]]) -> List[int]:
    """
    Codifica uma arvore rotulada pelo codigo de Prüfer em O(n).

    Ideia do algoritmo:

    1. Calculamos os graus atuais.
    2. Achamos a menor folha inicial com um ponteiro.
    3. Repetimos n - 2 vezes:
       - a variavel leaf guarda a menor folha atual;
       - encontramos seu unico vizinho ainda presente;
       - removemos leaf apenas no vetor de graus;
       - se o vizinho virou folha e tem rotulo menor que o ponteiro, ele e a
         proxima folha imediatamente;
       - senao, o ponteiro avanca ate a proxima folha.

    Por que O(n)?

    - Cada vertice vira leaf no maximo uma vez.
    - Ao processar uma leaf, percorremos sua lista de adjacencia original para
      achar o unico vizinho ativo; somando todas essas listas, temos O(n)
      entradas em uma arvore.
    - O ponteiro so anda para a direita; portanto, tambem soma O(n) passos.
    """
    adjacency = _validate_and_copy_tree(tree)
    n = len(adjacency)

    degree = [0] * (n + 1)
    for vertex in range(1, n + 1):
        degree[vertex] = len(adjacency[vertex])

    pointer = _first_leaf_from(degree, 1)
    leaf = pointer
    code: List[int] = []

    for _ in range(n - 2):
        parent = None
        for neighbor in adjacency[leaf]:
            if degree[neighbor] > 0:
                parent = neighbor
                break

        if parent is None:
            raise RuntimeError("Entrada invalida: folha sem vizinho ativo.")

        code.append(parent)

        degree[leaf] = 0
        degree[parent] -= 1

        if degree[parent] == 1 and parent < pointer:
            # Uma nova folha menor que o ponteiro deve ser usada agora.
            # O ponteiro nao volta; so a variavel leaf recebe esse rotulo.
            leaf = parent
        else:
            # Se a folha removida era menor que pointer, a folha em pointer
            # pode continuar disponivel. Por isso a busca recomeca em pointer,
            # nao em pointer + 1. Como pointer nunca diminui, o custo total
            # segue linear.
            pointer = _first_leaf_from(degree, pointer)
            leaf = pointer

    return code


def prufer_decode_linear(code: Sequence[int]) -> Tree:
    """
    Decodifica um codigo de Prüfer em uma arvore em O(n).

    Em um codigo de Prüfer, o grau final de um vertice v e:

        grau(v) = 1 + numero de ocorrencias de v no codigo.

    Entao os vertices que nao aparecem no codigo sao folhas. A cada simbolo x,
    conectamos a menor folha disponivel a x. A menor folha e mantida pela
    combinacao ponteiro + leaf descrita no topo do arquivo, sem heap.
    """
    prufer_code = _validate_and_copy_code(code)
    n = len(prufer_code) + 2

    degree = [1] * (n + 1)
    degree[0] = 0
    for label in prufer_code:
        degree[label] += 1

    pointer = _first_leaf_from(degree, 1)
    leaf = pointer
    tree: Tree = {vertex: [] for vertex in range(1, n + 1)}

    for label in prufer_code:
        tree[leaf].append(label)
        tree[label].append(leaf)

        degree[leaf] = 0
        degree[label] -= 1

        if degree[label] == 1 and label < pointer:
            # label acabou de virar folha e e menor que qualquer folha que
            # ainda sera encontrada pelo ponteiro.
            leaf = label
        else:
            # Se a folha removida era menor que pointer, a folha em pointer
            # pode continuar disponivel. Por isso a busca recomeca em pointer,
            # nao em pointer + 1.
            pointer = _first_leaf_from(degree, pointer)
            leaf = pointer

    remaining = [vertex for vertex in range(1, n + 1) if degree[vertex] == 1]
    if len(remaining) != 2:
        raise RuntimeError("Codigo invalido: a decodificacao nao terminou com duas folhas.")

    first_leaf, second_leaf = remaining
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
    """Casos de teste simples, executados com `python3 prufer_linear.py`."""
    two_vertices = make_tree(2, [(1, 2)])
    assert prufer_encode_linear(two_vertices) == []
    assert tree_edges(prufer_decode_linear([])) == tree_edges(two_vertices)

    path = make_tree(4, [(1, 2), (2, 3), (3, 4)])
    assert prufer_encode_linear(path) == [2, 3]
    assert tree_edges(prufer_decode_linear([2, 3])) == tree_edges(path)

    star = make_tree(5, [(4, 1), (4, 2), (4, 3), (4, 5)])
    assert prufer_encode_linear(star) == [4, 4, 4]
    assert tree_edges(prufer_decode_linear([4, 4, 4])) == tree_edges(star)

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
    assert prufer_encode_linear(slide_tree) == slide_code
    assert tree_edges(prufer_decode_linear(slide_code)) == tree_edges(slide_tree)

    exercise_code = [2, 3, 9, 5, 1, 8, 5, 2]
    exercise_tree = prufer_decode_linear(exercise_code)
    assert prufer_encode_linear(exercise_tree) == exercise_code

    # Este caso exercita o detalhe central da versao linear: depois que o
    # vertice 1 vira uma folha menor que o ponteiro, o ponteiro ainda deve
    # guardar a proxima folha ja encontrada.
    pointer_sensitive_code = [1, 1, 2, 2]
    pointer_sensitive_tree = prufer_decode_linear(pointer_sensitive_code)
    assert prufer_encode_linear(pointer_sensitive_tree) == pointer_sensitive_code

    try:
        prufer_encode_linear({1: [2], 2: [1], 3: []})
    except ValueError:
        pass
    else:
        raise AssertionError("Um grafo desconexo nao deve ser aceito.")

    print("Todos os testes da versao linear passaram.")


if __name__ == "__main__":
    _run_tests()

    print(prufer_encode_linear({1:[4,7,8],
                              2:[7],
                              3:[4],
                              4:[1,3,5],
                              5:[4],
                              6:[7],
                              7:[1,2,6],
                              8:[1]}))
    
    print(prufer_decode_linear([7, 4, 4, 1, 7, 1]))
    print(prufer_decode_linear([2, 3, 9, 5, 1, 8, 5, 2]))
