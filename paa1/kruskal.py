#!/usr/bin/python3

#### grafo de teste para Kruskal
#### descrito por uma lista de nodos e lista de arestas (com pesos)

v =  ['a','b','c','d','e', 'f', 'g']

e =  [ (('a','b'),1), 
       (('a','g'),2),
       (('a','f'),3), 
       (('b','c'),1),
       (('b','g'),2), 
       (('c','d'),4),
       (('c','g'),3),
       (('d','e'),2),
       (('d','g'),5),
       (('e','f'),6),
       (('e','g'),5),
       (('f','g'),4)]

    
#### versão simples do algoritmo de Kruskal
def kruskal(v,e):
	
	# ordena as arestas em ordem crescente de custo
	arestas = sorted(e, key=lambda x:x[1])
	
    
	# cria um dicionário para conter a informação de componente de nodos (p)
	# e um para o tamanho das partições (s)
	p = {}
	s = {}
	for i in v:
		p[i]=i
		s[i]=1
		    
	# determina n-1 inserções
	ins = len(v) - 1
       
	# lista de arestas do resultado
	res = []   
       
	# enquanto há arestas a inserir
	while ins>0 and len(arestas)>0:
		
		# remove a aresta de menor custo
		a = arestas.pop(0)
		
        # consulta os nodos da aresta
		x = a[0][0] # nodo1
		y = a[0][1] # nodo2
		
		# determina o componente de x e y, fazendo compressão de caminhos
		
		(m,n) = (x,y)
		ms = [m]  # nodos na rota de m
		ns = [n]  # nodos na rota de n
		while m != p[m]:
			m = p[m]
			ms.append(m)
		while n != p[n]:
			n = p[n]
			ns.append(n)
			
		# agora m e n são os nomes dos componentes de x e y
		
		# compressão de caminho
		for i in ms:
			p[i] = m
		for i in ns:
			p[i] = n
			
		# se estão no mesmo componente, 
		if m==n:
			continue   # não insere a aresta
	    
	    # se não estão no mesmo componente, 
		else:
			res = res + [a]  # insere a aresta no resultado
			
			# faz a menor partição apontar para a maior, atualizando o tamanho
			if s[m]<s[n]:         
				p[m]=n
				s[n] += s[m]    
			else:
				p[n]=m
				s[m] += s[n]
	    
			ins = ins-1      # contabiliza a inserção
		
	return res	# ao final, retorna a lista 
    

#### chamada de teste (Kruskal)
print(kruskal(v,e))
