;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-advanced-reader.ss" "lang")((modname exemplos_custo) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #t #t none #f () #f)))
;; Fundamentos de Algoritmos
;; Prof. Bruno Iochins Grisci
;;
;; Um algoritmo deve idealmente
;; 1. Sempre parar
;; 2. Com a resposta correta
;; 3. De forma eficiente
;;    Tempo?
;;    Espaço?
;;    Energia?
;;    Etc.
;;
;; Medimos esta eficiência em segundos? minutos? horas? dias? anos?
;;                            bytes? megabytes? gigabytes? terabytes?

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(display "--------------------------------------------------")

;; quantos?: Lista -> Número
;; Retorna o número de elementos na lista
(define (quantos? lista)
  ;; https://stackoverflow.com/questions/14326551/why-is-this-expression-giving-me-a-function-body-error
  (begin 
    (display "Chamando quantos? com lista = ") (display lista) (newline)
    (cond
     [( empty? lista) 0]
     [else (+ ( quantos? (rest lista )) 1)])) 
  )

(quantos? (list 'a 'b 'c))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;; Qual computação custará mais?

(display "--------------------------------------------------")

(quantos? (list 'a 'd 'b))

(quantos? (list 'a 'b 'c))

(quantos? (list 'b 'b 'b))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(display "--------------------------------------------------")

;; contém-b?: ListaDeSímbolos -> Booleano
;; Retorna verdadeiro caso o símbolo 'b exista na lista e falso caso contrário.
(define (contém-b? lds)
  (begin
   (display "Chamando contém-b? com lds = ") (display lds) (newline)
   (cond
    [( empty? lds) #false]
    [else (cond
           [( symbol=? (first lds) 'b) #true]
           [else (contém-b? (rest lds ))])])))

;; O número de passos necessários varia conforme a estrutura da
;; entrada. Considerar melhor caso, pior caso ou caso médio?
;;
;; O tempo de cada recursão é abstrato. Portanto, podemos ignorar
;; constantes e usar Ordens de Grandeza
;;
;; O número de passos (chamadas recursivas) para esta função chegar
;; ao resultado é, em média, N/2, sendo N o tamanho da entrada.
;; Este algoritmo é da ordem de N passos, ou O(N).
;;
;; Qual computação custará mais?

(contém-b? (list 'a 'd 'b))

(contém-b? (list 'a 'b 'c))

(contém-b? (list 'b 'b 'b))

(contém-b? empty)

;; Qual é o valor de N em cada caso?
;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(display "--------------------------------------------------")

;; insere: Número ListaDeNúmeros -> ListaDeNúmeros
;; Insere um novo número numa lista de números, colocando o novo número 
;; antes do primeiro elemento que for menor ou igual a ele
(define (insere n ldn)
  (begin
   (display "Chamando insere com n = ") (display n) (display "e ldn = ") (display ldn) (newline)  
   (cond
    [(empty? ldn) (cons n empty)]
    [else (cond
           [(>= n (first ldn )) (cons n ldn )]
           [(< n (first ldn )) (cons (first ldn)
                                     (insere n (rest ldn)))])])))

;; ordena: ListaDeNúmeros -> ListaDeNúmeros
;; Ordena uma lista de números em ordem decrescente
(define (ordena ldn)
  (begin
   (display "Chamando ordena com ldn = ") (display ldn) (newline)
   (cond
    [(empty? ldn) empty]
    [(cons? ldn) (insere (first ldn) (ordena (rest ldn )))])))

(ordena (list 3 1 2))

;; Sendo N o tamanho da lista de entrada, temos, em média:
;; O(N) chamadas de ordena
;; O(N**2) chamadas de insere

;; https://www.youtube.com/watch?v=ZZuD6iUe3Pc&list=PLLUEUvJhgJJDw5rGKmSFcA56Gyfejjh2Z&index=26&ab_channel=ViktorBohush

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(display "--------------------------------------------------")

;; maior: Lista-de-números -> Número
;; Determina o maior de uma lista não vazia de números
(define (maior ldn)
  (begin
   (display "Chamando maior com ldn = ") (display ldn) (newline) 
   (cond
    [(empty? (rest ldn )) (first ldn )]
    [else
     (cond
      [(> (maior (rest ldn )) (first ldn )) (maior (rest ldn ))]
      [else (first ldn )])])))

(maior (list 0 1 2 3))

(maior (list 1 2 3)) 

(maior (list 2 3))

(display "--------------------------------------------------")

;; maior2 : Lista-de-números -> Número
;; Determina o maior de uma lista não vazia de números
(define ( maior2 ldn)
  (begin
   (display "Chamando maior2 com ldn = ") (display ldn) (newline) 
   (cond
    [( empty? (rest ldn )) (first ldn )]
    [else (local (
                  (define maior-do-resto (maior2 (rest ldn ))) )
                 (cond
                  [(> maior-do-resto (first ldn )) maior-do-resto ]
                  [else (first ldn )]))])))

(maior2 (list 0 1 2 3))

(maior2 (list 1 2 3)) 

(maior2 (list 2 3))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Ordens de Grandeza








