#!/usr/bin/python3
"""Algoritmos de busca em grafos com representação por lista de adjacência.

- DFS recursivo
- DFS iterativo com pilha
- BFS por níveis e BFS com fila
- Construção de árvore pai via DFS
- Cálculo de distâncias
- Detecção de componentes conexos
- Detecção de ciclos em grafos não direcionados

"""

from collections import deque

# Esta versão usa `collections.deque` nas estruturas auxiliares das buscas.
# A motivação é evitar operações lineares na cabeça de listas Python:
# `pop(0)` e `insert(0, x)` custam O(n), pois exigem deslocar os elementos.
# Em `deque`, as operações nas extremidades custam O(1), o que combina melhor
# com pilhas, filas e inserções no início de sequências temporárias.
#
# Operações principais usadas neste arquivo:
# - `append(x)`: insere `x` à direita; em pilhas significa "empilhar" e em
#   filas significa "entrar no fim da fila".
# - `pop()`: remove da direita; nesta implementação representa desempilhar.
# - `appendleft(x)`: insere `x` à esquerda; aqui é usada quando queremos
#   construir uma ordem pelo início da sequência.
# - `popleft()`: remove da esquerda; nesta implementação representa retirar o
#   próximo elemento da fila.

#####################################################################

## Grafos/dígrafos como dicionários (lista de adjacências)


# dígrafo (acíclico)
g1 = {
    "A": ["B", "E"],
    "B": ["E", "F"],
    "C": ["D"],
    "D": [],
    "E": ["C", "F"],
    "F": ["D", "G"],
    "G": [],
}

# grafo simples (cíclico, nao bipartido, tres componentes conexos)
g2 = {
    "A": ["B"],
    "B": ["A", "D", "E"],
    "C": [],
    "D": ["B", "E"],
    "E": ["B", "D", "F"],
    "F": ["E"],
    "G": ["H"],
    "H": ["G"],
}

# dígrafo (cíclico)
g3 = {
    "A": ["B", "E"],
    "B": ["E"],
    "C": ["D"],
    "D": [],
    "E": ["C", "F"],
    "F": ["B", "D", "G"],
    "G": [],
}


# dígrafo (cíclico, quatro componentes fortemente conexos)
g4 = {
    1: [3],
    2: [4, 10],
    3: [5, 11],
    4: [7],
    5: [1, 7, 9],
    6: [10],
    7: [9],
    8: [6],
    9: [2, 4, 8],
    10: [8],
    11: [6, 8],
}


# dígrafo (acíclico)
g5 = {
    "A": ["B"],
    "B": ["C", "F"],
    "C": ["D"],
    "D": ["E"],
    "E": [],
    "F": ["E"],
    "G": ["H", "I"],
    "H": ["I", "F"],
    "I": [],
}


# grafo simples (cubo, bipartido, conexo)
g6 = {
    "000": ["100", "010", "001"],
    "001": ["101", "011", "000"],
    "010": ["110", "000", "011"],
    "100": ["000", "110", "101"],
    "011": ["111", "001", "010"],
    "101": ["001", "111", "100"],
    "110": ["010", "100", "111"],
    "111": ["011", "101", "110"],
}

# dígrafo (cíclico)
g7 = {
    "A": ["B"],
    "B": ["C", "F"],
    "C": ["D"],
    "D": ["E"],
    "E": [],
    "F": ["E"],
    "G": ["H"],
    "H": ["I", "F"],
    "I": ["G"],
}


#####################################################################

## Função que limpa registro de nós visitados
def clearVisited(v):
    """Reinicializa o mapa de visitados para reutilização.

    Args:
        v (dict): mapeamento nó -> status booleano visitado.
    """
    for i in list(v.keys()):
        v[i] = False


## Busca em profundidade (DFS)
def dfsRec(g, v, visited=None):  # g é um grafo, v é um nodo
    """Travessia em profundidade recursiva a partir de um nó inicial.

    Args:
        g (dict): representacao por lista de adjacencia.
        v: nodo inicial.
        visited (dict | None): mapa interno de visitados usado na recursão.
    """
    if visited is None:
        visited = {i: False for i in g.keys()}

    print(v)  # faça algo
    visited[v] = True  # registra que v foi visitado
    for i in g[v]:  # para todo vértice vizinho de v
        if not (visited[i]):
            dfsRec(g, i, visited)  # busca recursiva em cada vizinho não visitado


# dfsRec(g1,'A')


#####################################################################


## Busca em profundidade (DFS, iterativo com pilha)
def dfsStack(g, v):  # g é um grafo, v é um nodo
    """Travessia em profundidade iterativa usando pilha explícita.

    Args:
        g (dict): representacao por lista de adjacencia.
        v: nodo inicial.
    """
    visited = {}
    for i in g.keys():
        visited[i] = False  # lista de visitados
    l = deque([v])
    # inicia pilha unitária com v
    visited[v] = True  # registra que h foi visitado
    while len(l) > 0:  # enquanto há elementos em l
        h = l.pop()  # extrai em h o topo da pilha
        print(h)  # faça algo com h
        for i in g[h]:  # para vizinhos de h
            if not (visited[i]):  # se vizinho não visitado
                l.append(i)  # insere no topo da pilha
                visited[i] = True  # marca como visitado


## dfsStack(g1,'A')


#####################################################################


## Busca em largura (BFS, em níveis)
def bfsLevel(g, v):  # g é um grafo, v é um nodo
    """Calcula níveis de busca em largura a partir de um nó inicial.

    Args:
        g (dict): representacao por lista de adjacencia.
        v: nodo inicial.

    Returns:
        dict: mapeamento distancia -> lista de nós nesse nível.
    """
    visited = {}
    for i in g.keys():
        visited[i] = False  # vetor de visitados
    niveis = {}  # vetor de listas/niveis
    d = 0
    # nivel/distancia inicial
    niveis[d] = [v]  # inicializa nivel inicial
    visited[v] = True  # evita revisitar a origem em ciclos de retorno
    while len(niveis[d]) > 0:  # enquanto o nivel atual nao e vazio
        niveis[d + 1] = []  # inicia o proximo nivel
        for i in niveis[d]:  # para i = nodos do nivel atual
            for j in g[i]:  # para j = vizinhos destes
                if not (visited[j]):  # que não foram visitados
                    niveis[d + 1].append(j)  # insere vizinho j
                    visited[j] = True  # marca como visitado
        d += 1  # incrementa nivel atual
    return niveis


# print(bfsLevel(g1,'A'))


#####################################################################


## Busca em largura (BFS, iterativo com fila)
def bfsQueue(g, v):  # g é um grafo, v é um nodo
    """Travessia em largura usando semântica de fila.

    Args:
        g (dict): representacao por lista de adjacencia.
        v: nodo inicial.
    """
    visited = {}
    for i in g.keys():
        visited[i] = False  # lista de visitados

    l = deque([v])
    # inicia fila unitária com v
    visited[v] = True  # registra que h foi visitado

    while len(l) > 0:  # enquanto há elementos em l
        h = l.popleft()  # extrai em h a cabeça fila
        print(h)  # faça algo com h
        for i in g[h]:  # para vizinhos de h
            if not (visited[i]):  # se vizinho não visitado
                l.append(i)  # insere no final da fila
                visited[i] = True  # marca como visitado


# bfsQueue(g1,'A')


#####################################################################


## Árvore de busca em profundidade (DFS, iterativo com pilha)
def dfsStackTree(g, v):  # g é um grafo, v é um nodo
    """DFS iterativa que constrói mapeamento de pais.

    Args:
        g (dict): representacao por lista de adjacencia.
        v: nodo inicial.

    Returns:
        dict: mapeamento de pai para cada nó visitado.
    """
    parent = {}  # árvore de pais
    visited = {}
    for i in g.keys():
        visited[i] = False  # lista de visitados
        parent[i] = i  # autoreferência inicial
    l = deque([v])
    # inicia pilha unitária com v
    visited[v] = True  # registra que h foi visitado
    while len(l) > 0:  # enquanto há elementos em l
        h = l.pop()  # remove topo da pilha, e armazena em h
        print(h)  # faça algo com h
        for i in g[h]:  # para vizinhos de h
            if not (visited[i]):  # se vizinho não visitado
                l.append(i)  # insere no topo da pilha
                parent[i] = h  # marca h como pai de i
                visited[i] = True  # marca como visitado
    return parent  # retorna vetor de pais / reverso da árvore de busca


# print(dfsStackTree(g1,'A'))


#########################################

## Tabela de distancias a partir de um nodo


def bfsDistance(g, v):  # g é um grafo, v é um nodo
    """Calcula distância BFS para cada nó acessível.

    Args:
        g (dict): representacao por lista de adjacencia.
        v: nodo origem.

    Returns:
        dict: distancia da origem para cada nó, -1 para inacessível.
    """

    visited = {}  # nodos visitados
    dist = {}  # vetor de distâncias
    for i in g.keys():
        visited[i] = False  # inicializado em false
        dist[i] = -1  # inicializado em -1 (infinito)
    l = deque([v])
    # inicia lista unitária com v
    dist[v] = 0  # distancia até v é 0
    visited[v] = True  # marca v como visitado
    while len(l) > 0:  # enquanto há elementos em l
        h = l.popleft()  # remove cabeça da fila, e armazena em h
        visited[h] = True  # registra que h foi visitado
        for i in g[h]:  # para i = vizinhos de h
            if not (visited[i]):  # se i não foi visitado
                l.append(i)  # insere i no final de l
                dist[i] = dist[h] + 1  # atualiza distância de i
                visited[i] = True  # registra que passou por i
    return dist  # devolve vetor de distâncias


# print(bfsDistance(g1,'B'))


#####################################################################

## Componentes conexos


def connectedComponents(g):
    """Encontra componentes conexos em grafo não direcionado/implícito.

    Args:
        g (dict): representacao por lista de adjacencia.

    Returns:
        dict: mapeamento nó -> id do componente.
    """
    comp = {}  # vetor de componentes
    atual = 1  # componente inicial
    visited = {}  # nodos visitados
    for i in g.keys():
        visited[i] = False

    def dfsUCC(g, v):
        nonlocal comp, atual, visited
        visited[v] = True
        comp[v] = atual  # registra o componente atual
        for i in g[v]:
            if not (visited[i]):
                dfsUCC(g, i)

    for i in g.keys():
        if not (visited[i]):
            dfsUCC(g, i)  # busca o componente de i
            atual += 1  # incrementa componente
    return comp


# print(connectedComponents(g2))


#####################################################

## Testa se grafos simples é cíclico


def hasUndirectedCycle(g):
    """Detecta ciclo em grafo usando DFS.

    Funciona para grafos não direcionados com lista de adjacência.

    Args:
        g (dict): representacao por lista de adjacencia.

    Returns:
        bool: True se existir ciclo, False caso contrario.
    """
    parent = {}  # vetor de pais
    visited = {}  # vetor de visitados
    for i in g.keys():
        visited[i] = False  # inicializa com falso
        parent[i] = i  # autoreferência inicial

    for x in g.keys():
        if not visited[x]:
            l = deque([x])
            # inicia fila unitária com x
            visited[x] = True  # registra que h foi visitado
            while len(l) > 0:  # enquanto há elementos em l
                h = l.popleft()  # remove cabeça da fila, e armazena em h
                for i in g[h]:  # para todos os vizinhos de h
                    if not (visited[i]):  # i é vizinho não visitado
                        l.append(i)  # insere no fim da fila
                        parent[i] = h  # marca h como pai de i
                        visited[i] = True  # marca como visitado
                    elif (
                        i != parent[h]
                    ):  # i é vizinho visitado (e distinto do pai de h)
                        return True  # encontrou um ciclo

    return False  # não encontrou ciclo


# print(hasUndirectedCycle(g2))


#####################################################


## Teste de bipartição


def isBipartite(g):
    """Verifica se grafo não direcionado é bipartido usando 2-color BFS.

    Args:
        g (dict): representacao por lista de adjacencia.

    Returns:
        bool: True se bipartido (sem ciclo ímpar), False caso contrario.
    """
    cor = {}  # vetor de cores (True e False)
    visited = {}  # vetor de nodos visitados
    for i in g.keys():  # para todo nodo i em g
        visited[i] = False  # marca i nao visitado
    for x in g.keys():  # escolhe um nodo x por componente
        if not (visited[x]):  # se nao visitado
            l = deque([x])  # inicia a busca em x
            cor[x] = True  # atribui cor 1 a x
            visited[x] = True  # marca x como visitado
            while len(l) > 0:  # enquanto a nodos na busca
                i = l.popleft()  # remove o nodo da frente
                for j in g[i]:  # para todos os seus vizinhos
                    if (
                        visited[j] and cor[i] == cor[j]
                    ):  # se vizinho já colorido com cor oposta
                        return False  # achou ciclo impar
                    elif not (visited[j]):  # se vizinho ainda não colorido
                        l.append(j)  # adiciona a lista
                        visited[j] = True  # registra como visitado
                        cor[j] = not (cor[i])  # atribui cor inversa ao nodo atual
    return True  # se nao ha ciclo impar, o grafo e bipartido


# print(isBipartite(g6))


#####################################################

## Ordenamento topologico (DFS), devolve vetor de posições


def topoSortPositions(g):
    """Calcula ordenação topológica de um DAG como mapeamento de posições.

    Args:
        g (dict): representacao por lista de adjacencia.

    Returns:
        dict: no -> posicao topologica (1..n).
    """

    pos = {}  # vetor de posicoes
    atual = len(g.keys())  # posicao inicia em n
    visited = {}  # vetor de visitados
    for i in g.keys():  # com todos nodos
        visited[i] = False  # inicializados em falso

    def dfsTOPO(g, v):
        nonlocal atual, pos, visited
        visited[v] = True
        for i in g[v]:
            if not (visited[i]):
                dfsTOPO(g, i)  # navega a partir de v
        pos[v] = atual  # registra a posicao de v
        atual -= 1  # decrementa a posicao

    for i in g.keys():
        if not (visited[i]):
            dfsTOPO(g, i)  # inicia ordenamento

    return pos  # retorna o vetor de posicoes


# print(topoSortPositions(g1))


#####################################################


## Ordenamento topologico (DFS), devolve lista de nodos


def topoSortList(g):
    """Calcula ordenação topológica de um DAG como lista ordenada.

    Args:
        g (dict): representacao por lista de adjacencia.

    Returns:
        list: nos em ordem topologica.
    """

    pos = deque()  # lista de nodos

    visited = {}
    for i in g.keys():
        visited[i] = False

    def dfsTOPO(g, v):
        nonlocal pos, visited
        visited[v] = True
        for i in g[v]:
            if not (visited[i]):
                dfsTOPO(g, i)  # navega a partir de v
        pos.appendleft(v)  # insere v no topo da lista

    for i in g.keys():
        if not (visited[i]):
            dfsTOPO(g, i)  # inicia ordenamento

    return list(pos)  # retorna a lista de nodos em ordem topologica


# print(topoSortList(g5))


#####################################################

## Ordenamento topológico utilizando graus de entrada (Kahn 1962), devolve lista de nodos


def topoSortKahn(g):
    """Algoritmo de Kahn para ordenação topológica de um DAG.

    Args:
        g (dict): representacao por lista de adjacencia.

    Returns:
        list: ordem topologica dos nos.
    """
    inDeg = {}  # vetor de graus de entrada
    for i in g.keys():  # com todo nodo i
        inDeg[i] = 0  # grau de entrada 0
    for i in g.keys():  # para todo nodo i
        for j in g[i]:  # para j = vizinho de i
            inDeg[j] += 1  # incrementa grau de entrada de j
    q = deque()  # fila de nodos fonte (source)
    l = []  # lista de saída (ordenamento)
    for i in g.keys():
        if inDeg[i] == 0:
            q.append(i)  # inicializa q com nodos de grau 0
    while len(q) > 0:
        h = q.popleft()  # extrai h de q
        l.append(h)  # insere h em l
        for i in g[h]:  # para todos vizinho i de h
            inDeg[i] -= 1  # decrementa grau de i
            if inDeg[i] == 0:  # se grau chega a zero
                q.append(i)  # insere na lista de nodos fonte
    return l  # retorna a lista de nodos


# print(topoSortKahn(g5))


##########################################

## Reversao do grafo


def reverseGraph(g):
    """Retorna o grafo reverso de um grafo direcionado.

    Args:
        g (dict): lista de adjacencia de grafo direcionado.

    Returns:
        dict: lista de adjacencia do grafo invertido.
    """
    gRev = {}  # inicializa dicionário
    for i in g.keys():
        gRev[i] = []  # inicializa listas de adjacencias
    for i in g.keys():
        for j in g[i]:
            gRev[j].append(i)  # insere arcos reversos
    return gRev


# print(reverseGraph(g1))


##########################################


## componentes fortemente conexos (SCC, Kosaraju-Shamir)


def stronglyConnectedComponents(g):
    """Calcula componentes fortemente conexos em grafo direcionado.

    Args:
        g (dict): representacao por lista de adjacencia.

    Returns:
        dict: mapeamento nó -> id do componente.
    """
    gR = reverseGraph(g)  # reverte o grafo
    order = topoSortList(gR)  # calcula ordem de busca por gR
    comp = {}  # vetor de componentes
    atual = 1  # componente inicial
    visited = {}  # nodos visitados
    for i in g.keys():
        visited[i] = False

    def dfsSCC(g, v):  # busca em profundidade dos componentes
        nonlocal comp, atual, visited
        visited[v] = True
        comp[v] = atual  # registra o componente atual
        for i in g[v]:
            if not (visited[i]):
                dfsSCC(g, i)

    for i in order:  # na ordem adequada calculada via gR
        if not (visited[i]):
            dfsSCC(g, i)  # busca o componente de i
            atual += 1  # incrementa componente
    return comp  # retorna vetor de componentes


# print(stronglyConnectedComponents(g4))


############################################

## Testa se dígrafo possui ciclos


def hasDirectedCycle(g):
    """Detecta ciclo em grafo direcionado usando marcação de pilha de recursão.

    Args:
        g (dict): representacao por lista de adjacencia.

    Returns:
        bool: True se ciclo direcionado existir, False caso contrario.
    """
    inpath = {}  # marca nodos no caminho atual
    visited = {}  # nodos visitados globalmente
    cycle = False  # marca deteccao de ciclos

    for i in g.keys():
        visited[i] = False  # inicia sem visitados
        inpath[i] = False  # inicia sem nodos no caminho atual

    def dfsDC(g, v):
        nonlocal inpath, visited, cycle
        visited[v] = True  # marca v como visitado
        inpath[v] = True  # registra v no caminho atual
        for i in g[v]:
            if not visited[i]:  # explora nodos nao visitados
                dfsDC(g, i)
            elif inpath[i]:  # se i aponta para um nodo visitado no caminho atual
                cycle = True  # achou um ciclo
        inpath[v] = False  # remove  v do caminho atual

    for x in g.keys():  # para todos os nos do grafo
        if not visited[x]:  # se nodo nao visitado
            dfsDC(g, x)  # inicia busca a partir dele

    return cycle  #  retorna o resultado da busca do ciclo


# print(hasDirectedCycle(g1))


#####################################################################

## Aliases compatíveis com os nomes antigos

clear = clearVisited
dfs = dfsRec
dfsIter = dfsStack
bfs = bfsLevel
bfsIter = bfsQueue
dfsIterTree = dfsStackTree
distance = bfsDistance
components = connectedComponents
hasCycle = hasUndirectedCycle
bipartite = isBipartite
toposort = topoSortPositions
toposortList = topoSortList
toposortKahn = topoSortKahn
rev = reverseGraph
strongComponents = stronglyConnectedComponents
hasCycleDirected = hasDirectedCycle
