#!/usr/bin/python3


#####################################################################

## Grafo como dicionário
g1 = { 'A' : ['B', 'E'],
       'B' : ['E', 'F'],
       'C' : ['D'],
       'D' : [],
       'E' : ['C','F'],
       'F' : ['D','G'],
       'G' : []
      }

## Registro de nodos visitados pela busca
visited = {} 
for i in g1.keys():
	visited[i]=False


## Função que limpa registro de nós visitados
def clear(v):
	for i in list(v.keys()):
		v[i]=False


#####################################################################

## Busca em profundidade (DFS)

def dfs(g,v):       # g é um grafo, v é um nodo

	if visited[v]:  # se já visitei v: não faz nada e retorna
		return()

	print(v)        # faça algo
	visited[v]=True # registra que v foi visitado
	
	for i in g[v]:  # para todo vértice vizinho de v
		dfs(g,i)    # busca recursiva em cada vizinho não visitado
	

## chamada de teste	(DFS, recursivo)
#print("DFS(g1,A)\n\n")
#clear(visited)  
#dfs(g1,'A')	
#print("\n\n")



#####################################################################

## Busca em profundidade (DFS, iterativo)

def dfs2(g,v):   # g é um grafo, v é um nodo
	
	l = [v];    # inicia lista unitária com v
	
	while len(l)>0:    # enquanto há elementos em l

		h = l.pop(0)    # remove cabeça da lista, e armazena em h
		
		if visited[h]:
			continue    # se já visitado, desconsidera o vértice h
		print(h)        # faça algo com h
		visited[h]=True # registra que h foi visitado
		
		l = g[h] + l    # insere vizinhos de h no inicio de l, em ordem
			


## chamada de teste	(DFS, iterativo)
#print("DFS2(g1,A)\n\n")
#clear(visited)
#dfs2(g1,'A')	
#print("\n\n")



#####################################################################
	
## Busca em largura (BFS, iterativo)

def bfs(g,v):   # g é um grafo, v é um nodo
	
	l = [v];    # inicia lista unitária com v
	
	while len(l)>0:    # enquanto há elementos em l

		h = l.pop(0)    # remove cabeça da lista, e armazena em h
		
		if visited[h]:
			continue    # se já visitado, desconsidera o vértice h
		print(h)        # faça algo com h
		visited[h]=True # registra que h foi visitado
		
		l = l + g[h]    # insere vizinhos de h no final de l, em ordem


## chamada de teste	(BFS)
#print("BFS(g1,A)\n\n")
#clear(visited)
#bfs(g1,'A')	
#print("\n\n")

      
      
      
def conectado(g,a,b):  # determina se existe passeio de a para b
	
	# controle de nodos visitados
	visited = {} 
	for i in g.keys():
		visited[i]=False
		
	l = [a];    # inicia lista unitária com v
	
	while len(l)>0:    # enquanto há elementos em l

		h = l.pop(0)    # remove cabeça da lista, e armazena em h
		
		if visited[h]:
			continue    # se já visitado, desconsidera o vértice h
		
		if h==b:
			return True
		else:
			visited[h]=True # registra que h foi visitado
			l = g[h] + l    # insere vizinhos de h no inicio de l, em ordem		
	
	return False
      
      
#print("conectado(g1,F,A)\n\n")
#print(conectado(g1,'F','A'))	
#print("\n\n")
      


############################ distancia


def distancia(g,a,b):  # determina a distância entre a e b em g
	
	# controle de nodos visitados
	visited = {} 
	for i in g.keys():
		visited[i]=False
		
	l = [a];    # inicia lista unitária com v
	d = 0;      # distância inicial
		
	while len(l)>0:    # enquanto há elementos em l

		nl = [];    # próxima lista a ser considerada
		for h in l:
			if visited[h]:
				continue    # se já visitado, desconsidera o vértice h	
			if h==b:
				return d    # se já chegou, devolve d
			else:
				visited[h]=True # registra que h foi visitado
				for j in g[h]:  # insiro novos vizinhos não visitados
					if not visited[j]:
						nl = nl+[j]
		d = d+1
		l = nl		
		
	return 10**9
      
      
print("distance(g1,A,D)\n\n")
print(distancia(g1,'A','D'))	
print("\n\n")




#######################################3


def rota(g,a,b):  # determina se existe passeio de a para b
	
	# controle de nodos visitados
	visited = {} 
	for i in g.keys():
		visited[i]=False
		
	l = [a]     # inicia lista unitária com v
	
	parent = {} 
	for i in g.keys():
		parent[i]=i
	
	
	while len(l)>0:    # enquanto há elementos em l

		h = l.pop(0)    # remove cabeça da lista, e armazena em h
		
		if visited[h]:
			continue    # se já visitado, desconsidera o vértice h
		
		if h==b:
			nl = [b]
			h  = parent[b]
			while not (h==a):
				nl = [h]+nl
				h = parent[h]
			return [a]+nl	
			
		else:
			visited[h]=True # registra que h foi visitado
			l = g[h] + l    # insere vizinhos de h no inicio de l, em ordem		
			for i in g[h]:
				parent[i] = h
			
	return {}


print(rota(g1,'A','D'))


