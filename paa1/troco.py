"""Cashier's Algorithm - Greedy"""

from typing import List


def le_entrada():
    return float(input("Valor: "))

def greedy_troco(valor: float, moedas: List[int]):
    """Algoritmo guloso para o problema do troco."""
    moedas = sorted(moedas, reverse=True)
    troco = {m : 0 for m in moedas}
    valor *= 100
    while valor != 0:
        sem_solucao = True
        for m in moedas:
            if m <= valor:
                troco[m] += 1
                valor -= m
                sem_solucao = False
                break
        if sem_solucao:
            print("Sem solução!")
            return troco
    return troco


moedas = [1, 5, 10, 25, 50, 100]

valor = le_entrada()
while valor != -1:
    troco = greedy_troco(valor, moedas)
    print(troco)
    valor = le_entrada()
