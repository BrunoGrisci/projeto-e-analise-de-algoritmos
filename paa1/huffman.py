#!/usr/bin/python3

import heapq

# Le o arquivo de texto "alice.txt" contendo o livro "Alice no País das Maravilhas" (original em inglês)
# O arquivo precisa estar na mesma pasta do script, ou o caminho dele alterado no comando abaixo
with open("alice.txt", mode="r", encoding="utf-8") as f:
	data = f.read()
	
# dicionário/histograma de letras	
hist = {}	
out  = []

# processa a string de entrada, gerando uma lista de caracteres e convertendo símbolos UNICODE para símbolos correspondentes ASCII (0-127)
for i in range(len(data)):
	s = data[i]
	if (s=='”'):
		out.append('"')
	elif (s=='“'):
		out.append('"')
	elif (s=='—'):
		out.append('-')
	elif (s=='’'):
		out.append('\'')
	else:
		out.append(s)


# gera histograma da lista de caracteres ASCII obtida
for s in out:
	try:
		hist[s] += 1
	except KeyError:
		hist[s] = 1


'''

Descrição da estrutura de dados (baseada em pares ordenados aninhados)
para a representação de Sigma-árvores

arvore ::= ('node', leftTree, rightTree )
         | ('leaf', char)  
'''


# Implementação do algoritmo de Huffman usando árvores
def huffman(p):
	
	F = []   # floresta de árvores
		
	for i in p.keys():
		heapq.heappush(F,(p[i],('leaf',i)))  # inicializa floresta com árvores de tamanho 1
		
	while (len(F)>=2):              # enquanto há duas ou mais árvores na floresta
		(w1,a1) = heapq.heappop(F)  # extrai a árvore de menor peso
		(w2,a2) = heapq.heappop(F)  # extrai a próxima árvore de menor peso
		a3 = ('node', a1, a2)       # gera nova árvore 
		w3 = w1+w2                  # soma pesos
		heapq.heappush(F,(w3,a3))   # insere nova árvore na floresta
	
	return (F[0])[1]
	

# Conversão da árvore no código correspondente
def tree2code(t):
	c = {}
	if (t[0]=='leaf'):
		s = t[1]                                # s = letra da folha
		c[s] = ''                               # inicia o código de s com a string vazia
		return(c)                               # devolve o dicionário contendo s:""
	else:
		c1 = tree2code(t[1])                    # gera código para árvore da esquerda (c1)
		mc1 = { k:'0'+v  for k,v in c1.items()} # coloca '0' na frente dos valores (mc1)
		c2 = tree2code(t[2])                    # gera código para árvore da direita (c2)
		mc2 = { k:'1'+v  for k,v in c2.items()} # coloca '1' na frente dos valores (mc2)
		return( mc1 | mc2 )                     # devolve a união de dicionários mc1 e mc2



####################################################

# Distribuições para teste
h1 = { 'A':60, 'B':25, 'C':10, 'D':5 }
h2 = { 'A':3, 'B':2, 'C':6, 'D':8, 'E':2, 'F':6 }


# Constroi a codificação da Huffman com base na frequência de caracteres do texto original em inglês de "Alice no País das Maravilhas"

aliceCode = tree2code(huffman(hist))

# Contagem do tamanho (em bits) necessário para a codificação e o texto original
acc1 = 0
acc2 = 0
for s in out:
	acc1 += len(aliceCode[s])
	acc2 += 8
	
# Impressão do código gerado
print(tree2code(huffman(hist)))

# Tamanho do texto original e da versão comprimida (em bytes)
print("Tamanho do texto codificado: ", acc1/8)
print("Tamaho do texto em ASCII: ", acc2/8)
