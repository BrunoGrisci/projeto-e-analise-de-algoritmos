# Vetor desordenado		
l1 = [9,1,0,2,4,5,3,8,7,6]


# Variável para visualização do laço intermediário dos algoritmos
debug = True


##########################################################################

# INSERTION SORT

def insertionsort(A):
	n = len(A)
	for j in range(1,n):
		key = A[j]
		i = j-1
		while i>=0 and A[i]>key:
			A[i+1] = A[i]
			i = i-1
		A[i+1] = key
		if debug:
			print(A)
			input()
	


##########################################################################		
		
# SELECTION SORT		

def swap(A,x,y):
	tmp  = A[x]
	A[x] = A[y]
	A[y] = tmp


def selectionsort(A):
	n = len(A)
	for i in range(0,n):
		m = i
		for j in range(i,n):
			if A[j] < A[m]:
				m = j
		swap(A,i,m)
		if debug:
			print(A)
			input()


##########################################################################


# BUBBLE SORT		

def bubblesort(A):
	n = len(A)
	for i in range(0,n-1):
		for j in range(0,n-1-i):
			if A[j]>A[j+1]:
				swap(A,j,j+1)
		if debug:
			print(A)
			input()
		


##########################################################################


# MERGE SORT (versão imperativa)

aux = l1.copy()

def mergesort(A,p,r):
	if p<r:
		q = (p+r)//2
		if debug:
			print(A[p:r+1])
			print(A[p:q+1],A[q+1:r+1])
		mergesort(A,p,q)
		mergesort(A,q+1,r)
		if debug:
			print(A[p:q+1],A[q+1:r+1])
		merge(A,p,q,r)
		if debug:
			print(A[p:r+1])
		
	
def merge(A,start,mid,end):

	for i in range(start,end+1):
		aux[i] = A[i]
	i = start
	j = mid+1
	k = start
	while i<=mid and j<=end:
		if aux[i]<aux[j]:
			A[k] = aux[i]
			i += 1
		else:
			A[k] = aux[j]
			j += 1
		k += 1
	while i<=mid:
		A[k] = aux[i]
		i += 1
		k += 1
	while j<=end:
		A[k] = aux[j]
		j += 1
		k += 1
		

##########################################################################

# MERGE SORT (versão funcional)

def mergesort2(A):
	n = len(A)
	if n < 2:
		return A
	else:
		r1 = mergesort2(A[:n//2])
		r2 = mergesort2(A[n//2:])
		return  merge2(r1,r2)
		
def merge2(A,B):
	if len(A) == 0:
		return B
	if len(B) == 0:
		return A
	else:
		if A[0] < B[0]:
			return ([A[0]] + merge2(A[1:],B))
		else:
			return ([B[0]] + merge2(A,B[1:]))




##########################################################################

# QUICKSORT (versão imperativa)

def quicksort(A,p,r):
	if p<r:
		if debug:
			print(A[p:r+1])
		q = partition(A,p,r)
		if debug:
			print(A[p:q],A[q],A[q+1:r+1])
		quicksort(A,p,q-1)
		quicksort(A,q+1,r)

def partition(A,p,r):
	x = A[r]
	i = p-1
	for j in range(p,r):
		if A[j] <= x:
			i += 1
			swap(A,i,j)
	swap(A,i+1,r)
	return i+1

##########################################################################


# QUICK SORT (versão funcional)

def quicksort2(A):
	if len(A)<2:
		return A
	# extrai pivô	
	p = A[0]
	A = A[1:]
	# ordena recursivamente menores e maiores que pivô
	r1 = quicksort2(list(filter (lambda x: x<=p, A)))
	r2 = quicksort2(list(filter (lambda x: x>p, A)))
	# devolve lista ordenada
	return r1 + [p] + r2



# CHAMADAS

# insertionsort(l1)
# selectionsort(l1)
# bubblesort(l1)
# mergesort(l1,0,len(l1)-1)
# quicksort(l1,0,len(l1)-1)

# Impressao do vetor
print(l1)


# versões funcionais
# l2 = mergesort2(l1)
# l2 = quicksort2(l1)
# print(l2)
		
