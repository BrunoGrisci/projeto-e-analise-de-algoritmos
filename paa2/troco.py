"""Cashier's Algorithm - Dynamic Programming"""

from typing import Dict, List, Tuple


def le_entrada():
    return float(input("Valor: "))

def dp_troco(valor: float, moedas: List[int]) -> Tuple[int, List[int]]:
    """Algoritmo de programação dinâmica para o problema do troco.
    Retorna o número mínimo de moedas e os valores da DP.
    """
    moedas = sorted(moedas, reverse=True)
    valor = int(valor * 100)
    dp = [0 for _ in range(valor + 1)]

    dp[0] = 0
    for v in range(1, valor + 1):
        moedas_usaveis = [m for m in moedas if m <= v]
        # Bellman equation:
        dp[v] = min(dp[v - c] for c in moedas_usaveis) + 1
            
    return dp[valor], dp

def extrai_troco(dp: List[int], valor: float, moedas: List[int]) -> Dict[int,int]:
    """Dado os valores da DP, o valor de troco e as moedas, retorna o troco."""
    valor = int(valor * 100)
    troco = {m : 0 for m in moedas}
    while valor > 0:
        for m in moedas:
            if valor - m >= 0 and dp[valor] == dp[valor - m] + 1:
                troco[m] += 1
                valor -= m
                continue
    return troco

moedas = [1, 10, 21, 34, 70, 100, 350, 1225, 1500]

valor = le_entrada()
while valor != -1:
    min_moedas, dp = dp_troco(valor, moedas)
    print(extrai_troco(dp, valor, moedas))
    valor = le_entrada()
