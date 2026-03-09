'''Algoritmos de Ordenação'''

import random
import time
import matplotlib.pyplot as plt
import sys
import numpy as np

# Variável para visualização do laço intermediário dos algoritmos
debug = True

##########################################################################

# INSERTION SORT

def insertion_sort(array):
    n = len(array)
    for atual in range(1, n):
        chave = array[atual]
        anterior = atual - 1
        while anterior >= 0 and array[anterior] > chave:
            array[anterior + 1] = array[anterior]
            anterior -= 1
        array[anterior + 1] = chave

        if debug:
            print(array, anterior, atual)
            input()


##########################################################################

# SELECTION SORT


def swap(array, idx1, idx2):
    temp = array[idx1]
    array[idx1] = array[idx2]
    array[idx2] = temp


def selection_sort(array):
    n = len(array)
    for i in range(0, n):
        min_idx = i
        for j in range(i, n):
            if array[j] < array[min_idx]:
                min_idx = j
        swap(array, i, min_idx)
        if debug:
            print(array)
            input()


##########################################################################

# BUBBLE SORT


def bubble_sort(array):
    n = len(array)
    for i in range(0, n - 1):
        for j in range(0, n - 1 - i):
            if array[j] > array[j + 1]:
                swap(array, j, j + 1)
        if debug:
            print(array)
            input()


##########################################################################

# MERGE SORT (versão imperativa)

def merge_sort(array, aux, inicio, fim):
    if inicio < fim:
        meio = (inicio + fim) // 2
        if debug:
            print(array[inicio:fim + 1])
            print(array[inicio:meio + 1], array[meio + 1:fim + 1])
        merge_sort(array, aux, inicio, meio)
        merge_sort(array, aux, meio + 1, fim)
        if debug:
            print(array[inicio:meio + 1], array[meio + 1:fim + 1])
        merge(array, aux, inicio, meio, fim)
        if debug:
            print(array[inicio:fim + 1])


def merge(array, aux, inicio, meio, fim):
    for i in range(inicio, fim + 1):
        aux[i] = array[i]
    esquerda = inicio
    direita = meio + 1
    atual = inicio
    while esquerda <= meio and direita <= fim:
        if aux[esquerda] < aux[direita]:
            array[atual] = aux[esquerda]
            esquerda += 1
        else:
            array[atual] = aux[direita]
            direita += 1
        atual += 1

    while esquerda <= meio:
        array[atual] = aux[esquerda]
        esquerda += 1
        atual += 1
    while direita <= fim:
        array[atual] = aux[direita]
        direita += 1
        atual += 1


##########################################################################

# MERGE SORT (versão funcional)


def merge_sort_2(array):
    n = len(array)
    if n < 2:
        return array
    else:
        metade_esq = merge_sort_2(array[:n // 2])
        metade_dir = merge_sort_2(array[n // 2:])
        return merge_2(metade_esq, metade_dir)


def merge_2(left, right):
    merged = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    
    # Adicionar os restantes
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


##########################################################################

# QUICKSORT (versão imperativa)


def quick_sort(array, inicio, fim):
    if inicio < fim:
        if debug:
            print(array[inicio:fim + 1])
        pivo_idx = partition(array, inicio, fim)
        if debug:
            print(array[inicio:pivo_idx], array[pivo_idx], array[pivo_idx + 1:fim + 1])
        quick_sort(array, inicio, pivo_idx - 1)
        quick_sort(array, pivo_idx + 1, fim)


def partition(array, inicio, fim):
    pivo = array[fim]
    menores_idx = inicio - 1
    for atual in range(inicio, fim):
        if array[atual] <= pivo:
            menores_idx += 1
            swap(array, menores_idx, atual)
    swap(array, menores_idx + 1, fim)
    return menores_idx + 1


##########################################################################

# QUICK SORT (versão funcional)


def quick_sort_2(array):
    if len(array) < 2:
        return array
    # extrai pivô
    pivo = array[0]
    restante = array[1:]
    # ordena recursivamente menores e maiores que pivô
    menores = quick_sort_2(list(filter(lambda x: x <= pivo, restante)))
    maiores = quick_sort_2(list(filter(lambda x: x > pivo, restante)))
    # devolve lista ordenada
    return menores + [pivo] + maiores


def benchmark(quantidade_vetores=5, executar_lentos=False):
	# Aumentar limite de recursão
	sys.setrecursionlimit(50000)

	print("\n--- Teste de Desempenho ---")
	debug = False

	# Usaremos os valores exatos modificados pelo usuário
	ns_rapidos = [1000, 5000, 10000, 25000, 50000]
	ns_lentos = [1000, 2000, 5000, 10000, 25000] # O(n^2)

	algoritmos_lentos = ['Insertion', 'Selection', 'Bubble'] if executar_lentos else []
	algoritmos_rapidos = ['Merge\n(Imperat.)', 'Merge\n(Funcional)', 'Quick\n(Imperat.)', 'Quick\n(Funcional)']

	tempos_medias = {alg: [] for alg in algoritmos_lentos + algoritmos_rapidos}
	tempos_desvios = {alg: [] for alg in algoritmos_lentos + algoritmos_rapidos}
	ns_executados_lentos = []

	for n in ns_rapidos:
		
		resultados_rodadas = {alg: [] for alg in algoritmos_lentos + algoritmos_rapidos}

		# Rodar múltiplas vezes para calcular média e desvio
		for _ in range(quantidade_vetores):
			vetor_aleatorio = [random.randint(0, n) for _ in range(n)]
			
			# Algoritmos O(N log N)
			
			# Merge Sort (Imperativo)
			V = vetor_aleatorio.copy()
			aux_v = V.copy()
			inicio = time.time()
			merge_sort(V, aux_v, 0, len(V) - 1)
			resultados_rodadas['Merge\n(Imperat.)'].append(time.time() - inicio)

			# Merge Sort (Funcional)
			V = vetor_aleatorio.copy()
			inicio = time.time()
			merge_sort_2(V)
			resultados_rodadas['Merge\n(Funcional)'].append(time.time() - inicio)

			# Quick Sort (Imperativo)
			V = vetor_aleatorio.copy()
			inicio = time.time()
			quick_sort(V, 0, len(V) - 1)
			resultados_rodadas['Quick\n(Imperat.)'].append(time.time() - inicio)

			# Quick Sort (Funcional)
			V = vetor_aleatorio.copy()
			inicio = time.time()
			quick_sort_2(V)
			resultados_rodadas['Quick\n(Funcional)'].append(time.time() - inicio)
			
			# Algoritmos O(N^2)
			if n in ns_lentos and executar_lentos:
				# Insertion Sort
				V = vetor_aleatorio.copy()
				inicio = time.time()
				insertion_sort(V)
				resultados_rodadas['Insertion'].append(time.time() - inicio)

				# Selection Sort
				V = vetor_aleatorio.copy()
				inicio = time.time()
				selection_sort(V)
				resultados_rodadas['Selection'].append(time.time() - inicio)

				# Bubble Sort
				V = vetor_aleatorio.copy()
				inicio = time.time()
				bubble_sort(V)
				resultados_rodadas['Bubble'].append(time.time() - inicio)
				

		for alg in algoritmos_rapidos:
			tempos_medias[alg].append(np.mean(resultados_rodadas[alg]))
			tempos_desvios[alg].append(np.std(resultados_rodadas[alg]))

		if n in ns_lentos and executar_lentos:
			ns_executados_lentos.append(n)
			for alg in algoritmos_lentos:
				tempos_medias[alg].append(np.mean(resultados_rodadas[alg]))
				tempos_desvios[alg].append(np.std(resultados_rodadas[alg]))

		print(f"Testado N={n} (Média de {quantidade_vetores} vetores)")


	# Gerando o gráfico
	plt.figure(figsize=(10, 6))

	cores = {'Insertion': 'red', 'Selection': 'orange', 'Bubble': 'gold', 
			 'Merge\n(Imperat.)': 'lightgreen', 'Merge\n(Funcional)': 'green', 
			 'Quick\n(Imperat.)': 'lightblue', 'Quick\n(Funcional)': 'blue'}
	
	if executar_lentos:
		for alg in algoritmos_lentos:
			plt.errorbar(ns_executados_lentos, tempos_medias[alg], yerr=tempos_desvios[alg], fmt='-o', label=alg, color=cores[alg], capsize=5)

	for alg in algoritmos_rapidos:
		plt.errorbar(ns_rapidos, tempos_medias[alg], yerr=tempos_desvios[alg], fmt='-o', label=alg, color=cores[alg], capsize=5)

	plt.xlabel('n do Vetor (N)')
	plt.ylabel('Tempo Médio (segundos)')
	plt.title(f'Tempo de Execução dos Algoritmos de Ordenação (Média de {quantidade_vetores} Execuções)')
	plt.legend()
	plt.grid(True)
	
	plt.tight_layout()
	print("\nGerando gráfico de execução... Verifique a janela que se abrirá (ou será salva dependendo do SO).")
	plt.show()


if __name__ == "__main__":

	# Vetor desordenado
	l1 = [9, 1, 0, 2, 4, 5, 3, 8, 7, 6]
	aux = l1.copy()

	#insertion_sort(l1)
	#selection_sort(l1)
	#bubble_sort(l1)
	merge_sort(l1, aux, 0, len(l1) - 1)
	#quick_sort(l1, 0, len(l1) - 1)

	# Impressao do vetor
	print(l1)

	debug = False
	#benchmark()
