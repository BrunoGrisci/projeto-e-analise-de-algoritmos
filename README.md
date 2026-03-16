![Projeto e Análise de Algoritmos — header](assets/banner.png)

# Projeto e Análise de Algoritmos (INF05027/INF05028)

Repositório de códigos e exemplos para as disciplinas **INF05027 – Projeto e Análise de Algoritmos I** e **INF05028 – Projeto e Análise de Algoritmos II** do Instituto de Informática da UFRGS. O objetivo é concentrar implementações didáticas, exercícios e variações de algoritmos vistos em aula, facilitando o uso por diferentes alunos e professores ao longo do tempo.

As descrições de escopo abaixo foram extraídas das súmulas e conteúdos dos planos de ensino:
- PAA I: [`PlanodeEnsinoPAA1.pdf`](PlanodeEnsinoPAA1.pdf)
- PAA II: [`PlanodeEnsinoPAA2.pdf`](PlanodeEnsinoPAA2.pdf)

**Como ler o catálogo**
- Arquivos de um mesmo algoritmo são listados juntos.
- Cada entrada informa linguagem, autoria e uma frase de descrição.

## Projeto e Análise de Algoritmos I (INF05027)

**Escopo:** análise e corretude de algoritmos, notação assintótica, teoria dos grafos, algoritmos e estruturas de dados para grafos e algoritmos gulosos.

**Introdução**
| Algoritmo/Estrutura | Arquivos | Linguagem | Autor | Descrição |
| --- | --- | --- | --- | --- |
| Cashier's Algorithm | [https://github.com/BrunoGrisci/cashiers_algorithm_game](https://github.com/BrunoGrisci/cashiers_algorithm_game) | JavaScript | Bruno Iochins Grisci | Jogo educacional web para praticar e ensinar o problema de troco por meio de cenários interativos.|
| Karatsuba Multiplication Visualizer | [https://github.com/BrunoGrisci/karatsuba_visualization](https://github.com/BrunoGrisci/karatsuba_visualization) | JavaScript | Bruno Iochins Grisci | Implementação e comparação dos algoritmos de sala de aula e de Karatsuba para multiplicação de inteiros longos.|
| Gale–Shapley (emparelhamento estável) | [`galeshapley.py`](paa1/galeshapley.py) | Python | Bruno Iochins Grisci | Resolve o problema de emparelhamento estável e inclui exemplos e análise empírica. |
| Irving (stable roommates problem) | [`irving.py`](paa1/irving.py) | Python | Bruno Iochins Grisci | Resolve o problema de emparelhamento estável de colegas de quarto (um só grupo) e inclui exemplos e análise empírica. |
| Stable Matching Visualizer | [https://github.com/BrunoGrisci/stable-matching-visualizer](https://github.com/BrunoGrisci/stable-matching-visualizer) | JavaScript | Bruno Iochins Grisci | Ferramenta web para visualização do emparelhamento estável e algoritmos de Gale-Shapley e Irving. |
| Ordenamento | [`ordenamento.py`](paa1/ordenamento.py) | Python | Rodrigo Machado | Diversos algoritmos de ordenamento de vetores: InsertionSort, SelectionSort, BubbleSort, MergeSort, QuickSort.|
| Quicksort | [`quicksort.rkt`](paa1/quicksort.rkt) | Racket | Bruno Iochins Grisci | Ordena vetores de números de forma recursiva. |
| Algoritmo de Euclides | [`mdc.py`](paa1/mdc.py) | Python | Rodrigo Machado | Encontrar o Máximo Divisor Comum (MDC) de forma eficiente (e variações). |
| Exemplos diversos com custo | [`exemplos_custo.rkt`](paa1/exemplos_custo.rkt) | Racket | Bruno Iochins Grisci | Exemplos diversos recursivos para análise de custo. |

**Algoritmos para grafos**
| Algoritmo | Arquivos | Linguagem | Autor | Descrição |
| --- | --- | --- | --- | --- |
| Estruturas de dados para grafos | [`graph_example.ipynb`](paa1/graph_example.ipynb) | Python | Lucas Nunes Alegre | Demonstração de matriz de adjacência e lista de adjacência para grafos em Python. |
| Busca em grafos | [`graph-search-complete.py`](paa1/graph-search-complete.py) | Python | Rodrigo Machado | Algoritmos de busca em grafos: BFS, DFS, distância em grafos sem pesos, teste de ciclos, teste de bipartição, quantidade de componentes conexos, toposort, Kahn, Kosaraju-Shamir. |
| Busca em grafos | [`graph-search-bfs-dfs.py`](paa1/graph-search-bfs-dfs.py) | Python | Rodrigo Machado | Algoritmos de busca em grafos: BFS, DFS, distância em grafos sem pesos, teste de conexão, rota. |

**Algoritmos gulosos**
| Algoritmo | Arquivos | Linguagem | Autor | Descrição |
| --- | --- | --- | --- | --- |
| Intervalos | [`intervalos.py`](paa1/intervalos.py) | Python | Rodrigo Machado | Escalonamento de intervalos. Particionamento de intervalos. Minimização de atraso máximo. |
| Dijkstra (caminhos mínimos) | [`naivedijkstra.py`](paa1/naivedijkstra.py) | Python | Bruno Iochins Grisci | Calcula distâncias mínimas em grafos com pesos positivos (versão simples). |
| Dijkstra (caminhos mínimos) | [`heapdijkstra.py`](paa1/heapdijkstra.py) | Python | Bruno Iochins Grisci | Calcula distâncias mínimas em grafos com pesos positivos (versão com heap). |
| Dijkstra (caminhos mínimos) | [`dijkstra.py`](paa1/dijkstra.py) | Python | Rodrigo Machado | Calcula distâncias mínimas em grafos com pesos positivos (versão simples). |
| Heap mínimo (min-heap) | [`heap_demo.py`](paa1/heap_demo.py) | Python | Bruno Iochins Grisci | Demonstra operações de heap mínimo com visualização e rastreio didático. Observação: há um repositório dedicado em [https://github.com/BrunoGrisci/heap-demo](https://github.com/BrunoGrisci/heap-demo). |
| Kruskal | [`kruskal.py`](paa1/kruskal.py) | Python | Rodrigo Machado | Encontra a árvore geradora mínima. |
| Código de Huffman | [`huffman.py`](paa1/huffman.py) | Python | Rodrigo Machado | Constroi a codificação da Huffman com base na frequência de caracteres do texto original para compressão de texto. Usa como exemplo de entrada o texto original de Alice in Wonderland: [`alice.txt`](paa1/alice.txt).|

**Teoria dos grafos**
| Algoritmo | Arquivos | Linguagem | Autor | Descrição |
| --- | --- | --- | --- | --- |
| Hierholzer (caminho euleriano) | [`hierholzer.py`](paa1/hierholzer.py) | Python | Bruno Iochins Grisci | Encontra um caminho euleriano em grafo direcionado usando pilha explícita. |
| Welsh–Powell (coloração gulosa) | [`welsh_powell.py`](paa1/welsh_powell.py) | Python | Bruno Iochins Grisci | Colore vértices de um grafo usando ordenação por grau e estratégia gulosa. |

**Análise combinatória**
| Algoritmo | Arquivos | Linguagem | Autor | Descrição |
| --- | --- | --- | --- | --- |
| Princípios de contagem | [`Combinatoria.rkt`](combinatoria/Combinatoria.rkt) | Racket | Rodrigo Machado | Gera enumerações extensas de combinações, arranjos, permutações, combinações com reposição, arranjos com reposição, Triângulo de Pascal. |
| Permutações caóticas | [`chaotic_permutation.py`](combinatoria/chaotic_permutation.py) | Python | Bruno Iochins Grisci | Estima a probabilidade de uma permutação ser caótica (desarranjo) (uma permutação onde nenhum elemento permanece na mesma posição). Para n>2, essa proporção é 1/e. |
| Sequência de Tribonacci | [`tribonacci.py`](combinatoria/tribonacci.py) | Python | Bruno Iochins Grisci | Gera a sequência de Tribonacci. A sequência de Tribonacci é uma generalização da sequência de Fibonacci, onde cada termo é a soma dos três anteriores, começando por 0, 0, 1 (ou 0, 1, 1).|

## Projeto e Análise de Algoritmos II (INF05028)

**Escopo:** divisão e conquista, programação dinâmica, técnicas avançadas de projeto e estruturas de dados avançadas.

**Divisão e conquista**
| Algoritmo | Arquivos | Linguagem | Autor | Descrição |
| --- | --- | --- | --- | --- |
| Karatsuba Multiplication Visualizer | [https://github.com/BrunoGrisci/karatsuba_visualization](https://github.com/BrunoGrisci/karatsuba_visualization) | JavaScript | Bruno Iochins Grisci | Implementação e comparação dos algoritmos de sala de aula e de Karatsuba para multiplicação de inteiros longos.|
| Contagem de Inversões | [`inversions.cpp`](paa2/inversions.cpp) | C++ | Lucas Nunes Alegre | Implementa o algoritmo de contagem de inversões em um array usando Divisão e Conquista. |
| Par Mais Próximo (2D) | [`closest_pair.cpp`](paa2/closest_pair.cpp) | C++ | Lucas Nunes Alegre | Implementa o algoritmo de Par Mais Próximo em 2D usando abordagem de Divisão e Conquista. |

**Programação dinâmica**
| Algoritmo | Arquivos | Linguagem | Autor | Descrição |
| --- | --- | --- | --- | --- |
| Cashier's Algorithm | [https://github.com/BrunoGrisci/cashiers_algorithm_game](https://github.com/BrunoGrisci/cashiers_algorithm_game) | JavaScript | Bruno Iochins Grisci | Jogo educacional web para praticar e ensinar o problema de troco por meio de cenários interativos.|
| Edit Distance (Damerau-Levenshtein) | [`edit_distance.py`](paa2/edit_distance.py) | Python | Lucas Nunes Alegre | Implementa o algoritmo de distância de edição de Damerau-Levenshtein. |
| Bellman-Ford (caminhos mínimos) | [`bellman_ford.cpp`](paa2/bellman_ford.cpp) | C++ | Lucas Nunes Alegre | Implementa o algoritmo de Bellman-Ford para encontrar caminhos mínimos em grafos com arestas de peso negativo. |

**Tópicos avançados**
| Algoritmo | Arquivos | Linguagem | Autor | Descrição |
| --- | --- | --- | --- | --- |
| Em construção | — | — | — | Implementações previstas para esta subárea. |

## Licença

Este repositório é licenciado conforme o arquivo [`LICENSE`](LICENSE).

## Institucional

- Instituto de Informática (UFRGS): [https://www.inf.ufrgs.br](https://www.inf.ufrgs.br)
- Universidade Federal do Rio Grande do Sul (UFRGS): [https://www.ufrgs.br](https://www.ufrgs.br)

## Créditos e Contato Docente

- Prof. Bruno Iochins Grisci: [https://brunogrisci.github.io/](https://brunogrisci.github.io/)
- Prof. Lucas Nunes Alegre: [https://lucasalegre.github.io/](https://lucasalegre.github.io/)
- Prof. Rodrigo Machado: [https://www.inf.ufrgs.br/~rma/](https://www.inf.ufrgs.br/~rma/)

## Veja também
- [GitHub da disciplina de Fundamentos de Algoritmos](https://github.com/BrunoGrisci/fundamentos-de-algoritmos-racket.git)