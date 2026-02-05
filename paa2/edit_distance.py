"""
Implementação do algoritmo de distância de edição de Damerau-Levenshtein.
https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance

Lucas Nunes Alegre
Universidade Federal do Rio Grande do Sul
Instituto de Informática
Departamento de Informática Teórica
"""


def damerau_levenshtein(s1: str, s2: str) -> int:
    """Assumindo custo 1 para todas as operações."""

    len_s1 = len(s1)
    len_s2 = len(s2)
    
    # Cria uma matriz (len_s1+1) x (len_s2+1)
    dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]
    
    # Inicializa a matriz
    for i in range(len_s1 + 1):
        dp[i][0] = i
    for j in range(len_s2 + 1):
        dp[0][j] = j
    
    # Preenche a matriz
    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            
            dp[i][j] = min(
                dp[i - 1][j] + 1,        # deletar
                dp[i][j - 1] + 1,        # inserir
                dp[i - 1][j - 1] + cost  # substituir
            )
            
            # Verifica transposição (troca de dois caracteres adjacentes)
            if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                dp[i][j] = min(dp[i][j], dp[i - 2][j - 2] + 1)  # transposição

    operations = reconstruct_damerau_operations(s1, s2, dp)

    return dp[len_s1][len_s2], operations


def reconstruct_damerau_operations(s1, s2, dp):
    i, j = len(s1), len(s2)
    operations = []

    while i > 0 or j > 0:
        current = dp[i][j]

        # Caso substituição ou match
        if i > 0 and j > 0:
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            if dp[i - 1][j - 1] + cost == current:
                if cost == 1:
                    operations.append(f"Substitute '{s1[i-1]}' with '{s2[j-1]}' at position {i-1}")
                i -= 1
                j -= 1
                continue

        # Caso transposição
        if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
            if dp[i - 2][j - 2] + 1 == current:
                operations.append(f"Transpose '{s1[i - 2]}' and '{s1[i - 1]}' at positions {i - 2} and {i - 1}")
                i -= 2
                j -= 2
                continue

        # Caso inserção
        if j > 0 and dp[i][j - 1] + 1 == current:
            operations.append(f"Insert '{s2[j - 1]}' at position {i}")
            j -= 1
            continue

        # Caso deleção
        if i > 0 and dp[i - 1][j] + 1 == current:
            operations.append(f"Delete '{s1[i - 1]}' from position {i - 1}")
            i -= 1
            continue

    operations.reverse()
    return operations


if __name__ == "__main__":
    s1 = "kitten"
    s2 = "sitting"
    distance, ops = damerau_levenshtein(s1, s2)
    print(f"Edit Distance: {distance}")
    print("Operations:")
    for op in ops:
        print(op)

    s1 = "DACTG"
    s2 = "DACTG"
    distance, ops = damerau_levenshtein(s1, s2)
    print(f"Edit Distance: {distance}")
    print("Operations:")
    for op in ops:
        print(op)
