import heapq
import time 
from itertools import permutations

# Intervalos de exemplo

# escalonamento
interv_a = [ (0,9), (1,2), (3,4), (5,6), (7,8) ]
interv_b = [ (0,5), (6,10), (4,7) ]
interv_c = [ (0,2), (1,4), (1,4), (1,4), (3,6), (5,8), (7,10), (9,12), (9,12), (9,12), (11,14) ]

# particionamento
interv_d = [ (0,11), (0,1), (2,5), (7,10), (0,3), (4,6), (8,12), (13,16), (14,15) ]

# minimização do atraso
interv_e = [ ('a',3,6), ('b',2,8), ('c',1,9), ('d',4,9), ('e',3,14), ('f',2,15) ]


####################################################################################
###         Escalonamento de intervalos 
####################################################################################

# determina um subconjunto máximo de intervalos compatíveis
def terminaMaisCedo(l):
	lista = sorted(l,key=lambda x:x[1])               # ordena lista de intervalos pelo segundo componente (fim)
	a     = [lista.pop(0)]                            # lista de intervalos selecionados, inicializada com o primeiro intervalo
	
	while len(lista)>0:                               # enquanto há intervalos a serem processados

		h = lista.pop(0)                              # remove o primeiro

		if h[0] > a[0][1]:                            # se o intervalo h é compatível com o último inserido na solução
			a.insert(0,h)                             # insere intervalo na solução
	return a
	
	
#print(terminaMaisCedo(interv_a))



####################################################################################
###         Particionamento de intervalos 
####################################################################################

# determina um conjunto de salas mínimo que permita a execução de todos os intervalos de ocupação da lista
def iniciaMaisCedo(l):
	lista = sorted(l,key=lambda x:x[0])    # ordena lista de intervalos pelo primeiro componente (inicio)
	aloca = {}                             # dicionário sala => lista de tarefas (última inserida é colocada na frente)
	while len(lista)>0:
		x = lista.pop(0)                   # x é a tarefa  de menor tempo de inicio
		# Determina uma sala livre para inserir x. Se não houver, cria sala nova	
		achou = False
		i     = 0
		for i in aloca.keys():           # para todas as salas disponíveis
			if aloca[i][0][1] <= x[0]:   # se a ocupação da sala (segundo componente do primeiro item da lista) termina antes do inicio da tarefa x
				aloca[i].insert(0,x)     # registra a alocação de x na sala atual (inserindo na frente da lista)
				achou = True             # marca que achou
				break 
		if not(achou):                   # se não achou sala disponível
			aloca[len(aloca)] = [x]      # cria nova sala e insere x nela
	return aloca
	



#print(iniciaMaisCedo(interv_d))
#start_time = time.time() 
#a = iniciaMaisCedo([(0,1)]*10000)
#end_time = time.time()
#print(a)
#print(end_time - start_time, " segundos")



# determina um conjunto de salas mínimo que permita a execução de todos os intervalos de ocupação da lista
def iniciaMaisCedoHeap(l):
	
	lista = sorted(l,key=lambda x:x[0])    # ordena lista de intervalos pelo primeiro componente (inicio)
	
	aloca = []                             # heap contendo tripla (tempo-liberacao, nro sala, lista de tarefas). Chave = tempo-liberacao
	
	h    = lista.pop(0)                    # extrai primeiro intervalo h
	heapq.heappush(aloca,(h[1],0,[h]))     # inicializa a heap com ele

	while len(lista)>0:
		
		x = lista.pop(0)                   # x é a tarefa  de menor tempo de inicio

		(f,s,l) = aloca[0]                 # acessa o primeiro elemento da heap (elemento de f mínimo), sem remover

		if x[0] <= f:                      # se o início de x conflita com o término mínimo de salas, não há sala disponível
			n = len(aloca)                       # cria novo nome de sala
			heapq.heappush(aloca, (x[1],n,[x]))  # insere x na nova sala (na heap)

		else:                                 # se não há conflito, atualizar sala s na heap, incluindo x e atualizando f como 
			heapq.heappop(aloca)              # remove o primeiro elemento da lista
			l.insert(0,x)                     # adiciona x à lista de s
			heapq.heappush(aloca,(x[1],s,l))  # inclui a atualização na heap

	return aloca
	

#start_time = time.time() 
#a = iniciaMaisCedoHeap(interv_d)
#end_time = time.time()
#print(a)
#print(end_time - start_time, " segundos")




####################################################################################
###         Minimização de atraso máximo
####################################################################################


# determina um escalonamento que minimiza atraso máximo
def minimizaAtraso(l):
	
	lista = sorted(l,key=lambda x:x[2])               # ordena lista de intervalos (nome,duracao,deadline) pelo terceiro componente (deadline)
	t     = 0                                         # tempo de registro das tarefas
	a     = []                                        # lista de intervalos selecionados, inicializada com o primeiro intervalo
	while len(lista)>0:                               # enquanto há intervalos a serem processados
		h = lista.pop(0)                              # remove o primeiro intervalo
		a.append((h[0],t,t+h[1]))                     # aloca a tarefa x no intervalo (t, t+duracao), gerando tripla (x,t,t+duracao) na saida
		t = t + h[1]                                  # atualiza o tempo atual
	return a                                          # devolve saida
	
	
print(minimizaAtraso(interv_e))
