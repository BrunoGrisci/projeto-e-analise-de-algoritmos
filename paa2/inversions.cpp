/*
Algoritmo para contar o número de inversões em um array usando Divisão e Conquista.
https://en.wikipedia.org/wiki/Inversion_(discrete_mathematics)#Counting_inversions

Lucas Nunes Alegre
Universidade Federal do Rio Grande do Sul
Instituto de Informática
Departamento de Informática Teórica
*/

#include <iostream>
#include <vector>

using namespace std;

// Função que faz o merge e conta inversões cruzadas
pair<vector<int>, int> MergeAndCountSplitInv(const vector<int>& A, const vector<int>& B) {
    vector<int> L;
    int inv = 0;
    int i = 0, j = 0;
    int nA = A.size(), nB = B.size();

    while (i < nA && j < nB) {
        if (A[i] <= B[j]) {
            L.push_back(A[i]);
            i++;
        } else {
            L.push_back(B[j]);
            inv += (nA - i); // Todos os elementos restantes em A formam inversão com B[j]
            j++;
        }
    }

    while (i < nA) {
        L.push_back(A[i]);
        i++;
    }

    while (j < nB) {
        L.push_back(B[j]);
        j++;
    }

    return {L, inv};
}

// Função recursiva que divide e conta as inversões
pair<vector<int>, int> MergeAndCountInversions(vector<int> &S){
    int n = S.size();
    if (n <= 1) {
        return {S, 0};
    }

    int mid = n / 2;
    vector<int> A(S.begin(), S.begin() + mid);
    vector<int> B(S.begin() + mid, S.end());

    auto [A_sorted, invA] = MergeAndCountInversions(A);
    auto [B_sorted, invB] = MergeAndCountInversions(B);
    auto [L, invCross] = MergeAndCountSplitInv(A_sorted, B_sorted);

    int totalInversions = invA + invB + invCross;

    return {L, totalInversions};
}

// Exemplo de uso
int main() {
    vector<int> S;
    int number;

    while (cin >> number) {
        S.push_back(number);
    }

    auto [sortedArray, totalInversions] = MergeAndCountInversions(S);

    cout << "Numero total de inversões: " << totalInversions << endl;
    cout << "Array ordenado: ";
    
    for (int x : sortedArray) {
        cout << x << " ";
    }
    cout << endl;

    return 0;
}
