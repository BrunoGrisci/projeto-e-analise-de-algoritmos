# Bruno Iochins Grisci
# October 30, 2023

# Este código estima a probabilidade de uma permutação ser caótica (desarranjo)
# Para isto ele gera aleatoriamente {rep} permutações de um arranjo de tamanho {n}
# E calcula quantas destas {rep} permutações são caóticas dentro do total de {rep} permutações

import numpy as np

def is_chaotic(perm):
    # Subtraindo o arranjo permutado pelo ordenado, basta contar quanas posições foram zeradas.
    # O único caso em que pode haver zeros no arranjo da diferença é quando os valores naquela posição
    # eram iguais, ou seja, o elemento ficou na mesma posição,
    a_range = np.arange(perm.size)
    return (np.count_nonzero((perm - a_range)==0) == 0) # conta se há zeros no arranjo de diferença, devolve false se sim

def main():
    rep = 10000 # número de repetições
    n = 30 # comprimento do arranjo
    counter = 0
    for i in range(rep):
        a = np.random.permutation(n) # cria um arranjo aleatório permutado entre 0 e n-1
        if is_chaotic(a):
            counter = counter+1
    prob = counter / rep # quanto maior for rep, mais próxima a prob fica de 1/e (aprox. 0.367879441), independentemente do tamanho de n

    print("Probabilidade estimada de ser uma permutação caótica em {} sequências de tamanho {}: {}".format(rep, n, prob))


if __name__ == '__main__': 
    main()