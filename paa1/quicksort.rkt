;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-advanced-reader.ss" "lang")((modname quicksort) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #t #t none #f () #f)))
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Prof. Bruno Iochins Grisci
;; INF05008 - Fundamentos De Algoritmos
;; Baseado nos slides da Prof. Leila Ribeiro
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; https://www.youtube.com/watch?v=x1FwLc8kPoE&ab_channel=LeilaRibeiro

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Uma ListaDeNúmeros pode ser
;; 1. vazia (empty), ou
;; 2. (cons e l) , onde
;; e : Número
;; l : ListaDeNúmeros

;; maiores: ListaDeNúmeros Número -> ListaDeNúmeros
;; Dados um numero e uma lista de números, devolve todos os elementos da lista maiores que este número.
;; Exemplo: 
;; (maiores (list 11 14 7) 8) = (list 11 14)
(define (maiores lista n)
  (cond
   [(empty? lista) empty]
   [(> (first lista) n) (cons (first lista) (maiores (rest lista) n))]
   [else (maiores (rest lista) n)]))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; menores: ListaDeNúmeros Número -> ListaDeNúmeros
;; Dados um numero e uma lista de números, devolve todos os elementos da lista menores que este número.
;; Exemplo: 
;; (maiores (list 11 14 7) 8) = (list 7)
(define (menores lista n)
  (cond
   [(empty? lista) empty]
   [(< (first lista) n) (cons (first lista) (menores (rest lista) n))]
   [else (menores (rest lista) n)]))

;; Daria para usar filter?

(let ((first (car (list 7 5 1 6 9 8 12 854 -8 4 0 9)))) ; get the first element
        (filter (lambda (x) (> x first)) (cdr (list 7 5 1 6 9 8 12 854 -8 4 0 9)))) ; filter elements larger than the first

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; _quicksortERRADO: ListaDeNúmeros -> ListaDeNúmeros
;; Dada uma lista de números, ordenar a lista em ordem crescente.
;; Exemplo: 
;; (_quicksort (list 11 8 14 7)) = (list 7 8 11 14)
(define (_quicksortERRADO l)
  (cond
   ;; Se a lista l estiver vazia, retornar a própria lista vazia.
   [(empty? l) empty]
   ;; Senão
   [else ;; Juntar as seguintes listas:
    (append
     ;; a lista ordenada dos elementos da lista l menores que o primeiro
     (_quicksortERRADO (menores l (first l)))
     ;; a lista que contém somente o primeiro elemento da lista
     (list (first l))
     ;; a lista ordenada dos elementos da lista l maiores que o primeiro
     (_quicksortERRADO (maiores l (first l)))
     )
    ]
   )
  )

(_quicksortERRADO (list 7 5 1 6 9 8 12 854 -8 4 0))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(_quicksortERRADO (list 7 5 1 6 9 8 12 854 -8 4 0 9)) ;; O que deu errado?

;; Usar >= resolveria?

;; iguais: ListaDeNúmeros Número -> ListaDeNúmeros
;; Dados um numero e uma lista de números, devolve todos os elementos da lista iguais a este número.
;; Exemplo: 
;; (iguais (list 11 14 7 14) 8) = emtpy
;; (iguais (list 11 14 7 14) 14) = (list 14 14)
(define (iguais lista n)
  (cond
   [(empty? lista) empty]
   [(= (first lista) n) (cons (first lista) (iguais (rest lista) n))]
   [else (iguais (rest lista) n)]))

(define (_quicksortREP l)
  (cond
   ;; Se a lista l estiver vazia, retornar a própria lista vazia.
   [(empty? l) empty]
   ;; Senão
   [else ;; Juntar as seguintes listas:
    (append
     ;; a lista ordenada dos elementos da lista l menores que o primeiro
     (_quicksortREP (menores l (first l)))
     ;; a lista que contém somente o primeiro elemento da lista
     (list (first l))
     (iguais (rest l) (first l))
     ;; a lista ordenada dos elementos da lista l maiores que o primeiro
     (_quicksortREP (maiores l (first l)))
     )
    ]
   )
  )

(_quicksortREP (list 7 5 1 6 9 8 12 854 -8 4 0))
(_quicksortREP (list 7 5 1 6 9 8 12 854 -8 4 0 9))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; Definida na linguagem:

(quicksort (list 7 5 1 6 9 8 12 854 -8 4 0 9) <)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;