debug = True

#####################################################################

# Algoritmo trivial, versão 1
def mdc1(a,b):
	steps = 0
	m = 1
	for x in range(1,min(a,b)+1):
		steps += 1
		if debug:
			print(steps, " : testando ",x)
		if a%x==0 and  b%x==0:
			m = x
	if debug:
			print("MDC = ",m)
	return m


#####################################################################

# Algoritmo trivial, versão 2
def mdc2(a,b):
	steps = 0
	x = min(a,b)
	while x>0:
		steps += 1
		if debug:
			print(steps, " : testando ",x)
		if a%x==0 and  b%x==0:
			if debug:
				print("MDC = ",x)
			return x
		x -= 1

#####################################################################

# Algoritmo de euclides (primeira versão, usando subtração)
def euclides1(a,b):
	steps = 0
	while (a!=0 and b!=0):
		steps += 1
		if debug:
			print(steps, ": testando", a, b)
		if a>=b:
			(a,b) = (a-b,b)
		else:
			(a,b) = (b-a,a)
	if a==0:
		if debug:
			print("MDC = ",b)
		return b
	else:
		if debug:
			print("MDC = ",a)
		return a


#####################################################################

# Algoritmo de euclides (segunda versão, usando o resto da divisão inteira)
def euclides2(a,b):
	steps = 0
	while (a!=0 and b!=0):
		steps += 1
		if debug:
			print(steps, ": testando", a, b)
		if a>=b:
			(a,b) = (b,a%b)
		else:
			(a,b) = (a,b%a)
	if a==0:
		if debug:
			print("MDC = ",b)
		return b
	else:
		if debug:
			print("MDC = ",a)
		return a
 


# Caso de teste 1: 1020 e 402015		
		
#x = mdc1(1020,402015)
#x = mdc2(1020,402015)
#x = euclides1(1020,402015)
#x = euclides2(1020,402015)


# Caso de teste 2: 9086721347 e 10234703240

#x = mdc1(9086721347,10234703240)
#x = mdc2(9086721347,10234703240)
#x = euclides1(9086721347,10234703240)
#x = euclides2(9086721347,10234703240)


# Caso de teste 3: 86047438501520378390232 e 23648200008403340502

#x = mdc1(86047438501520378390232,23648200008403340502)
#x = mdc2(86047438501520378390232,23648200008403340502)	
#x = euclides1(86047438501520378390232,23648200008403340502)
#x = euclides2(86047438501520378390232,23648200008403340502)	
