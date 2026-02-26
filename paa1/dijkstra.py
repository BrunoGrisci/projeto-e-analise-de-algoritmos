#!/usr/bin/python3

#### grafo de teste para Dijkstra

g2 = { 'U' : ['A','B'],
       'A' : ['U', 'C', 'D'],
       'B' : ['U', 'D', 'C'],
       'D' : ['A','B','E'],
       'C' : ['B','A','E'],
       'E' : ['C','D'],
       'F' : []
      }


#### pesos das arestas presentes
weight = { ('U','A') : 1,
           ('U','B') : 3,
           ('A','U') : 1,
           ('A','C') : 4,
           ('A','D') : 5,
           ('B','U') : 3,
           ('B','D') : 4,
           ('B','C') : 5,
           ('D','A') : 5,
           ('D','B') : 4,
           ('D','E') : 2,
           ('C','B') : 5,
           ('C','A') : 4,
           ('C','E') : 6,
           ('E','D') : 2,
           ('E','C') : 6
         }
         
#### função de pesos das arestas
def w(a,b):
	if  (a,b) in weight.keys():
		return weight[(a,b)]
	else:
		return 10**9  # representando infinito
    

#### testa se todos os nodos em s possuem distância infinita em t
def allInf(t,s):
	for i in s:
		if t[i]<10**9:
			return False
	return True
   

#### versão simples do algoritmo de Dijkstra
def dijkstra(g,u):
	
	# inicializa a tabela t
	t = {}
	for v in list(g.keys()):
		if v==u:
			t[v]=0
		else:
			t[v]=w(u,v)
			
	# inicializa o conjunto s de chaves a serem inseridas
	s = set(g.keys())
	s.remove(u) 
	
	while not ( (len(s)==0) or allInf(t,s) ): # enquanto há nodos a incluir
	
		# busca o vértice em s de menor valor m em t, e armazena em c
		c = list(s)[0];
		for j in s:
			if t[j]<t[c]:
				c = j
		
		# remove c dos nodos a serem inseridos
		s.remove(c)		
		
		# atualiza a tabela de distâncias com triangularizações via c
		for z in s:
			t[z] = min(t[z],t[c]+w(c,z))
			
	# retorna a tabela de distâncias
	return t


#### chamada de teste (Dijkstra)
print("DIJKSTRA(g2,A)\n\n")
print(dijkstra(g2,'A'))
print("\n\n")


