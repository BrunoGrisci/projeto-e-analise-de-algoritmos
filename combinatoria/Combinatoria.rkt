;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-advanced-reader.ss" "lang")((modname Combinatoria) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #t #t none #f () #f)))
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;                 FUNÇÕES AUXILIARES                      ;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; fact : numero -> numero
;; (fact 5) => 120
(define (fact n)
  (cond
    [(<= n 0)  1]
    [else (* n (fact (- n 1)))]))

;; prefixaTodos : lista-de-X   lista-de-lista-de-X -> lista-de-lista-de-X
;; (prefixaTodos (list 'X 'Y) (list (list 'a 'b) (list 'c 'd))) => (list (list 'X 'Y 'a 'b) (list 'X 'Y 'c 'd))
(define (prefixaTodos a l)
   (map (lambda (x) (append a x)) l))

;; concat : lista-de-lista-de-X -> lista-de-X
;; (concat (list (list 1 2) (list 5) (list 3 4))) => (list 1 2 5 3 4)
(define (concat l) 
  (foldr append empty l))

;; chooseOne : lista-de-X -> lista-de-lista-de-X
;; (chooseOne (list 1 2 3)) => (list (list 1 2 3) (list 2 1 3) (list 3 1 2))
;; gera todas as possíveis escolhas de elementos de l, colocando o elemento
;; escolhido como primeiro elemento de cada lista.
(define (chooseOne l)
  (map (lambda (x) (cons x (remove x l))) l))  

;; genNumbers: numero -> lista-de-numeros
;; (genNumbers 5) => (list 0 1 2 3 4 5)
(define (genNumbers n)
  (local ((define (genAux x)
            (cond
              [(<= x n) (cons x (genAux (+ x 1)))]
              [else     empty])))
    
    (genAux 0))) 


;; genPosNumbers: numero -> lista-de-numeros
(define (genPosNumbers n)
  (cond
    [(< n 1) empty]
    [else (rest (genNumbers n))]))

;; genRepeatList: X numero -> lista-de-X
;; (genRepeatList 'a 4) => (list 'a 'a 'a 'a)
(define (genRepeatList n s)
  (cond
    [(<= n 0) empty]
    [else (cons s (genRepeatList (- n 1) s))]))

;; genMultiList: X numero -> lista-de-listas-de-X
;; (genMultiList 'a 3) => (list (list ) (list 'a) (list 'a 'a) (list 'a 'a 'a))
(define (genMultiList n s)
   (map
     (lambda (x) (genRepeatList x s))
     (genNumbers n)))







;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;                 COMBINAÇÕES                             ;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


;; comb: número lista-de-X -> lista-de-lista-de-X
;; (comb k l) gera todas os conjuntos de tamanho k
;; com elementos tirados da lista l, assumindo que 
;; a lista l não possui repetições
(define (comb k l)
 (cond
  [(<= k 0)   (list (list ))] ;; conjunto vazio
  [(empty? l) (list )       ] ;; não há conjunto não-vazio sobre alfabeto vazio
  [else (append               ;; união de dois coleções de conjuntos
          (comb k (rest l))   ;; -> todos os k-conjuntos sem (first l)
          (prefixaTodos       ;; -> todos os (k-1)-conjuntos com (first l)
             (list (first l))
             (comb (- k 1) (rest l)))) ]))
;; exemplo:
;; (comb 2 (list 1 2 3 4))
;; => (list (list 3 4) 
;;          (list 2 4) 
;;          (list 2 3) 
;;          (list 1 4) 
;;          (list 1 3) 
;;          (list 1 2))


;; c : numero numero -> numero
;; (c k n) calcula o número de combinações de tamanho k 
;; sobre alfabeto de tamanho n
(define (c k n)
  (cond
    [(<= k 0) 1]
    [(<= n 0) 0]
    [else  (/ (fact n) (* (fact k) (fact (- n k))))]))






;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;                    ARRANJOS                             ;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


;; arr : numero lista-de-X -> lista-de-lista-de-X
;; (arr k l) gera todos os arranjos de tamanho k, 
;; gerados a partir do alfabeto l
(define (arr k l)
  (cond
    [(<= k 0)    (list (list) )]  
    [(empty? l)  (list) ]         
    [else (concat 
           (map
             (lambda (c)       
               (prefixaTodos (list (first c)) (arr (- k 1) (rest c))))
             (chooseOne l)))])) 



;; a : numero numero -> numero
;; (a k n) calcula o número de arranjos de tamanho k sobre
;; alfabeto de tamanho n
(define (a k n)
  (cond
    [(<= k 0) 1]
    [(<= n 0) 0]
    [else  (/ (fact n) (fact (- n k)))]))









;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;          COMBINAÇÕES COM REPOSIÇÃO                      ;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


;; combR: número lista-de-X -> lista-de-lista-de-X
;; (combR k l) gera todos os multiconjuntos de tamanho k
;; com elementos tirados da lista l, considerando que cada
;; elemento de l pode ser utilizado repetidamente

(define (combR k a)
 (cond
  [(<= k 0)          (list (list ))]                     ;; conjunto vazio
  [(empty? a)        (list )       ]                     ;; alfabeto vazio
  [else              (concat (map
                               (lambda (x) 
                                    (prefixaTodos 
                                        (genRepeatList x (first a))
                                        (combR (- k x) (rest a))))
                               (genNumbers k)))]))
         

;; cR : número número -> número
;; (cR k n) calcula o número de combinações com repetição de tamanho k
;; sobre um alfabeto de tamanho n
(define (cR k n)
  (c k (+ k n -1)))
  
  




;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;             ARRANJOS COM REPOSIÇÃO                      ;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


;; arrR : numero lista-de-X -> lista-de-lista-de-X
;; (arrR k l) gera todos os arranjos de tamanho k, 
;; gerados a partir do alfabeto l, permitindo repetição
;; no arranjo
(define (arrR k l)
  (cond
    [(<= k 0)    (list (list) )]  
    [(empty? l)  (list) ]         
    [else (concat 
           (map
             (lambda (c)       
               (prefixaTodos (list (first c)) (arrR (- k 1) c)))
             (chooseOne l)))])) 

;; aR : número número -> número
;; (aR k n) calcula o número de palavras de tamanho k
;; sobre um alfabeto de tamanho n
(define (aR k n)
  (expt n k))






;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;                   PERMUTAÇÕES                           ;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;



;;; Implementação utilizando arr

;;; perm: lista-de-X : lista-de-lista-de-X
;;; (perm l) calcula todas as permutações dos elementos da lista l
(define (perm l)
  (arr (length l) l))
;; (perm2 (list 1 2 3))
;; => (list (list 1 2 3) 
;;          (list 2 1 3) 
;;          (list 2 3 1) 
;;          (list 1 3 2) 
;;          (list 3 1 2) 
;;          (list 3 2 1))     


;; p : número -> número
(define (p n)
  (fact n))



;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;                 TRIÂNGULO DE PASCAL                     ;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;; (linhaPascal n)  gera a n-ésima linha do triângulo de pascal
(define (linhaPascal n)
  (map (lambda(x) (c x n)) (genNumbers n)))

;; (pascal n) gera o triângulo de pascal até linha n
(define (pascal n)
  (map linhaPascal (genNumbers n)))




