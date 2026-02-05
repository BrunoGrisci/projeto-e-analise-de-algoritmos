/*
Algoritmo de Bellman-Ford para encontrar o caminho mais curto em um grafo com arestas de peso negativo.
https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm

Lucas Nunes Alegre
Universidade Federal do Rio Grande do Sul
Instituto de Informática
Departamento de Informática Teórica
*/

#include <iostream>
#include <limits.h>
#include <vector>
#include <stack>

using namespace std;

// Estrutura para representar uma aresta no grafo
struct Edge {
    int source, destination, weight;
};

// Função para imprimir o caminho completo da origem até o vértice destino
void printPath(int vertex, const vector<int>& predecessor) {
    stack<int> path;
    int current = vertex;
    
    // Subir pelos predecessores até a origem ou não encontrar caminho
    while (current != -1) {
        path.push(current);
        current = predecessor[current];
    }

    // Imprimir o caminho
    cout << "Path: ";
    while (!path.empty()) {
        cout << path.top();
        path.pop();
        if (!path.empty()) cout << " -> ";
    }
    cout << endl;
}

// Função para executar o algoritmo de Bellman-Ford
void bellmanFord(vector<Edge>& graph, int vertices, int source) {
    vector<int> distance(vertices, INT_MAX);
    vector<int> predecessor(vertices, -1); // <-- Predecessores
    distance[source] = 0;

    // Relaxar todas as arestas |V| - 1 vezes
    for (int i = 0; i < vertices - 1; i++) {
        for (const Edge& e : graph) {
            if (distance[e.source] != INT_MAX &&
                distance[e.source] + e.weight < distance[e.destination]) {
                distance[e.destination] = distance[e.source] + e.weight;
                predecessor[e.destination] = e.source; // <-- Armazena predecessores
            }
        }
    }

    // Verificar ciclos de peso negativo
    for (const Edge& e : graph) {
        if (distance[e.source] != INT_MAX &&
            distance[e.source] + e.weight < distance[e.destination]) {
            cout << "Graph contains negative weight cycle" << endl;
            return;
        }
    }

    // Imprimir distâncias e caminhos
    cout << "Vertex\tDistance from Source\tPath\n";
    for (int i = 0; i < vertices; ++i) {
        cout << i << "\t";
        if (distance[i] == INT_MAX) {
            cout << "INF\t\t\tNo path\n";
        } else {
            cout << distance[i] << "\t\t\t";
            printPath(i, predecessor); // <-- Imprime o caminho completo
        }
    }
}

int main() {
    int vertices = 6;

    vector<Edge> graph = {
        {0, 1, 5}, {0, 2, 7}, {1, 2, 3},
        {1, 3, 4}, {1, 4, 6}, {3, 4, -1},
        {3, 5, 2}, {4, 5, -3}
    };

    bellmanFord(graph, vertices, 0);

    return 0;
}
